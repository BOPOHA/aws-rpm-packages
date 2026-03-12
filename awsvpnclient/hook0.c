#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
#include <sys/socket.h>
#include <stdint.h>

/*
 * DBus Boolean Hook (hook0.c) - Multi-part Socket Interception (v7)
 * 
 * HOW IT WORKS:
 * This library uses LD_PRELOAD to intercept socket-related system calls
 * (sendmsg, sendto, write) and modifies DBus messages in transit.
 * 
 * The hook specifically targets DBus method return messages (type 2) that
 * correspond to the IsExclusiveAppInstance method call and forces the
 * boolean result to true (1).
 * 
 * It handles two message patterns:
 * 1. Multi-part messages: Where DBus header is in one buffer (iov[0]) and
 *    the body containing the boolean is in a separate buffer (other iov).
 *    The header is parsed to verify the method and reply serial.
 * 
 * 2. Single-buffer messages: Complete DBus message in one buffer.
 *    Parses the message structure to locate the boolean value in the body.
 * 
 * USAGE:
 * Compile as shared library:
 *   gcc -shared -fPIC -o hook0.so hook0.c -ldl
 * 
 * Inject into target application:
 *   LD_PRELOAD=./hook0.so /path/to/application
 * 
 * The hook intercepts outgoing socket data before it's sent, modifies it,
 * then passes it to the original system call.
 */

__attribute__((constructor))
static void init_hook() {
    fprintf(stderr, "[HOOK] Intercepting sendmsg, sendto, and write system calls\n");
}

static uint32_t recent_serials[32];
static size_t recent_serials_pos = 0;

static int has_serial(uint32_t serial) {
    size_t count = sizeof(recent_serials) / sizeof(recent_serials[0]);
    for (size_t i = 0; i < count; i++) {
        if (recent_serials[i] == serial) return 1;
    }
    return 0;
}

static void record_serial(uint32_t serial) {
    if (has_serial(serial)) return;
    recent_serials[recent_serials_pos % (sizeof(recent_serials) / sizeof(recent_serials[0]))] = serial;
    recent_serials_pos++;
}

static int consume_serial(uint32_t serial) {
    size_t count = sizeof(recent_serials) / sizeof(recent_serials[0]);
    for (size_t i = 0; i < count; i++) {
        if (recent_serials[i] == serial) {
            recent_serials[i] = 0;
            return 1;
        }
    }
    return 0;
}

static uint32_t read_u32(const unsigned char *p, int is_le) {
    if (is_le) {
        return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
    }
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) | ((uint32_t)p[2] << 8) | (uint32_t)p[3];
}

static size_t align_up(size_t v, size_t a) {
    return (v + (a - 1)) & ~(a - 1);
}

typedef struct {
    int is_le;
    uint8_t type;
    uint32_t serial;
    const unsigned char *fields;
    uint32_t fields_len;
} header_info;

static int parse_header_info(const unsigned char *buf, size_t len, header_info *out) {
    if (len < 16) return 0;
    if (buf[0] != 'l' && buf[0] != 'B') return 0;
    out->is_le = (buf[0] == 'l');
    out->type = buf[1];
    out->serial = read_u32(buf + 8, out->is_le);
    out->fields_len = read_u32(buf + 12, out->is_le);
    if ((size_t)out->fields_len + 16 > len) return 0;
    out->fields = buf + 16;
    return 1;
}

static int header_find_string_field(const header_info *hi, uint8_t code, char *out, size_t out_len) {
    size_t pos = 0;
    while (pos < hi->fields_len) {
        size_t struct_start = align_up(pos, 8);
        if (struct_start + 1 > hi->fields_len) return 0;
        pos = struct_start;

        uint8_t field_code = hi->fields[pos];
        size_t v = pos + 1;
        if (v >= hi->fields_len) return 0;

        uint8_t sig_len = hi->fields[v++];
        if (v + sig_len >= hi->fields_len) return 0;
        const unsigned char *sig = hi->fields + v;
        v += sig_len + 1; // include NUL

        if (sig_len == 1 && sig[0] == 's') {
            size_t val_off = align_up(v, 4);
            if (val_off + 4 > hi->fields_len) return 0;
            uint32_t str_len = read_u32(hi->fields + val_off, hi->is_le);
            val_off += 4;
            if (val_off + str_len + 1 > hi->fields_len) return 0;

            if (field_code == code && out_len > 0) {
                size_t copy_len = str_len < (out_len - 1) ? str_len : (out_len - 1);
                memcpy(out, hi->fields + val_off, copy_len);
                out[copy_len] = '\0';
                return 1;
            }

            size_t value_end = val_off + str_len + 1;
            pos = align_up(value_end, 8);
            continue;
        }

        // Skip unsupported variant types
        pos = align_up(v, 8);
    }
    return 0;
}

static int header_find_u32_field(const header_info *hi, uint8_t code, uint32_t *out) {
    size_t pos = 0;
    while (pos < hi->fields_len) {
        size_t struct_start = align_up(pos, 8);
        if (struct_start + 1 > hi->fields_len) return 0;
        pos = struct_start;

        uint8_t field_code = hi->fields[pos];
        size_t v = pos + 1;
        if (v >= hi->fields_len) return 0;

        uint8_t sig_len = hi->fields[v++];
        if (v + sig_len >= hi->fields_len) return 0;
        const unsigned char *sig = hi->fields + v;
        v += sig_len + 1; // include NUL

        if (sig_len == 1 && sig[0] == 'u') {
            size_t val_off = align_up(v, 4);
            if (val_off + 4 > hi->fields_len) return 0;
            if (field_code == code) {
                *out = read_u32(hi->fields + val_off, hi->is_le);
                return 1;
            }
            size_t value_end = val_off + 4;
            pos = align_up(value_end, 8);
            continue;
        }

        // Skip unsupported variant types
        pos = align_up(v, 8);
    }
    return 0;
}

static int should_force_true_for_buffer(const unsigned char *buf, size_t len, uint32_t *out_reply_serial) {
    header_info hi;
    if (!parse_header_info(buf, len, &hi)) return 0;

    if (hi.type == 1) {
        char member[128];
        if (header_find_string_field(&hi, 3, member, sizeof(member)) && strcmp(member, "IsExclusiveAppInstance") == 0) {
            record_serial(hi.serial);
            fprintf(stderr, "[HOOK] Observed IsExclusiveAppInstance call, serial=%u\n", hi.serial);
        }
        return 0;
    }

    if (hi.type == 2) {
        uint32_t reply_serial = 0;
        if (header_find_u32_field(&hi, 5, &reply_serial)) {
            if (consume_serial(reply_serial)) {
                if (out_reply_serial) *out_reply_serial = reply_serial;
                return 1;
            }
        }
    }

    return 0;
}

static void force_boolean_true(unsigned char *buf, size_t len, const char *syscall_name, int part_idx) {
    if (len < 4) return;
    buf[0] = 1;
    buf[1] = 0;
    buf[2] = 0;
    buf[3] = 0;
    fprintf(stderr, "[HOOK] Forced boolean true in %s part %d\n", syscall_name, part_idx);
}

static void process_buffer(unsigned char *buf, size_t len, const char *syscall_name, int part_idx) {
    if (len < 1) return;

    uint32_t reply_serial = 0;
    if (!should_force_true_for_buffer(buf, len, &reply_serial)) return;

    if (len >= 16 && (buf[0] == 'l' || buf[0] == 'B')) {
        int is_le = (buf[0] == 'l');
        uint32_t header_fields_len = read_u32(buf + 12, is_le);
        size_t body_start = 16 + header_fields_len;
        body_start = align_up(body_start, 8);

        if (body_start + 4 <= len) {
            fprintf(stderr, "[HOOK] Intercepted IsExclusiveAppInstance reply (serial=%u) in %s (single-buf) at offset %zu\n",
                    reply_serial, syscall_name, body_start);
            force_boolean_true(buf + body_start, len - body_start, syscall_name, part_idx);
        }
    }
}

typedef ssize_t (*orig_sendmsg_t)(int sockfd, const struct msghdr *msg, int flags);
ssize_t sendmsg(int sockfd, const struct msghdr *msg, int flags) {
    static orig_sendmsg_t orig = NULL;
    if (!orig) orig = dlsym(RTLD_NEXT, "sendmsg");

    if (msg->msg_iovlen >= 1) {
        unsigned char *first = (unsigned char *)msg->msg_iov[0].iov_base;
        size_t first_len = msg->msg_iov[0].iov_len;
        uint32_t reply_serial = 0;

        // Track IsExclusiveAppInstance calls and detect matching replies from the first iov.
        int should_force = should_force_true_for_buffer(first, first_len, &reply_serial);
        if (should_force && msg->msg_iovlen >= 2) {
            int forced = 0;
            for (int i = 1; i < (int)msg->msg_iovlen; i++) {
                unsigned char *body = (unsigned char *)msg->msg_iov[i].iov_base;
                size_t body_len = msg->msg_iov[i].iov_len;
                if (body_len >= 4) {
                    fprintf(stderr, "[HOOK] Intercepted IsExclusiveAppInstance reply (serial=%u) in sendmsg multi-buf\n", reply_serial);
                    force_boolean_true(body, body_len, "sendmsg", i);
                    forced = 1;
                    break;
                }
            }
            if (!forced) {
                fprintf(stderr, "[HOOK] Reply matched but no body buffer found in sendmsg (serial=%u)\n", reply_serial);
            }
        }
    }

    for (int i = 0; i < (int)msg->msg_iovlen; i++) {
        process_buffer((unsigned char *)msg->msg_iov[i].iov_base, msg->msg_iov[i].iov_len, "sendmsg", i);
    }

    return orig(sockfd, msg, flags);
}

typedef ssize_t (*orig_sendto_t)(int sockfd, const void *buf, size_t len, int flags, const struct sockaddr *dest_addr, socklen_t addrlen);
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags, const struct sockaddr *dest_addr, socklen_t addrlen) {
    static orig_sendto_t orig = NULL;
    if (!orig) orig = dlsym(RTLD_NEXT, "sendto");

    process_buffer((unsigned char *)buf, len, "sendto", 0);

    return orig(sockfd, buf, len, flags, dest_addr, addrlen);
}

typedef ssize_t (*orig_write_t)(int fd, const void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count) {
    static orig_write_t orig = NULL;
    if (!orig) orig = dlsym(RTLD_NEXT, "write");

    process_buffer((unsigned char *)buf, count, "write", 0);

    return orig(fd, buf, count);
}
