#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <dlfcn.h>
#include <string.h>
#include <dirent.h>
#include <ctype.h>
#include <stdlib.h>
#include <fcntl.h>
#include <limits.h>
#include <stdarg.h>

/*
 * Multi-User Detection Hook (hook8.c) - Comprehensive Tracing
 * 
 * OVERALL STRATEGY:
 * This LD_PRELOAD hook library intercepts system calls to debug how applications
 * detect multiple active users on the system. The goal is to identify
 * which system information sources are checked (utmp/wtmp, /proc, D-Bus, etc.) and potentially
 * spoof them to bypass multi-user detection restrictions.
 * 
 * The hook combines multiple approaches:
 * - Force root privileges to eliminate UID-based checks
 * - Trace execve() to catch external command executions (who, w, loginctl, etc.)
 * - Monitor file opens for user databases (utmp, wtmp, /run/user/*, /etc/passwd)
 * - Intercept Unix socket connections to detect D-Bus queries
 * - Hide processes in /proc to make the system appear single-user
 * 
 * Goal: Find exactly how applications detect "Multiple active users".
 */

__attribute__((constructor))
static void init() {
    fprintf(stderr, "[DEBUG_LOG] Multi-user detection hook loaded into PID %d\n", getpid());
}

// 1. Force root privileges
// 
// WHAT IT DOES: Always returns UID 0 (root) regardless of actual user
// WHY: Applications might check if processes belong to different UIDs to detect
// multiple users. By making everything appear as root, we eliminate UID-based detection.
// HOW IT WORKS: Intercepts getuid() syscall and returns 0 instead of the real UID.
typedef uid_t (*getuid_func)();
uid_t getuid(void) {
    static getuid_func real_getuid = NULL;
    if (!real_getuid) real_getuid = (getuid_func)dlsym(RTLD_NEXT, "getuid");
    return 0; 
}

// 2. Trace execve to see if it's calling external commands
//
// WHAT IT DOES: Logs all program executions with their full command-line arguments
// WHY: Applications might execute system utilities to check for users:
//      - 'who' or 'w' - shows logged-in users
//      - 'loginctl' - systemd login manager (lists sessions)
//      - 'users' - prints logged-in user names
// HOW IT WORKS: Intercepts execve() and prints the pathname and all argv[] entries
// to stderr before passing through to the real execve().
typedef int (*orig_execve_t)(const char *pathname, char *const argv[], char *const envp[]);
int execve(const char *pathname, char *const argv[], char *const envp[]) {
    static orig_execve_t orig = NULL;
    if (!orig) orig = dlsym(RTLD_NEXT, "execve");
    
    fprintf(stderr, "[DEBUG_LOG] execve(\"%s\")\n", pathname);
    int i = 0;
    while(argv && argv[i]) {
        fprintf(stderr, "  argv[%d]: %s\n", i, argv[i]);
        i++;
    }
    return orig(pathname, argv, envp);
}

// 3. Trace open to see if it's reading utmp/wtmp or similar
//
// WHAT IT DOES: Logs opens of files that contain user/session information
// WHY: These files are common sources for detecting logged-in users:
//      - /var/run/utmp - currently logged-in users
//      - /var/log/wtmp - login/logout history
//      - /run/user/* - per-user runtime directories (indicates active sessions)
//      - /etc/passwd, /etc/group - user account databases
// HOW IT WORKS: Filters open() calls by pathname, logs suspicious files to stderr,
// then passes through to real open(). Handles variadic arguments for O_CREAT mode.
typedef int (*orig_open_t)(const char *pathname, int flags, ...);
int open(const char *pathname, int flags, ...) {
    static orig_open_t orig = NULL;
    if (!orig) orig = dlsym(RTLD_NEXT, "open");

    if (strstr(pathname, "utmp") || strstr(pathname, "wtmp") || strstr(pathname, "run/user") || strstr(pathname, "/etc/passwd") || strstr(pathname, "/etc/group")) {
        fprintf(stderr, "[DEBUG_LOG] open(\"%s\", %d)\n", pathname, flags);
    }

    if (flags & (O_CREAT | O_TMPFILE)) {
        va_list args;
        va_start(args, flags);
        mode_t mode = va_arg(args, mode_t);
        va_end(args);
        return orig(pathname, flags, mode);
    }
    return orig(pathname, flags);
}

// 4. Trace connect to see if it's connecting to system D-Bus
//
// WHAT IT DOES: Logs all Unix domain socket connections
// WHY: Applications might query systemd/D-Bus for session information:
//      - org.freedesktop.login1 - systemd-logind (ListSessions, ListUsers)
//      - /var/run/dbus/system_bus_socket - system D-Bus
//      - abstract sockets - private IPC
// HOW IT WORKS: Intercepts connect() for AF_UNIX sockets, extracts the path from
// sockaddr_un (handles both path-based and abstract sockets), logs it, then proceeds.
#include <sys/socket.h>
#include <sys/un.h>
typedef int (*orig_connect_t)(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
    static orig_connect_t orig = NULL;
    if (!orig) orig = dlsym(RTLD_NEXT, "connect");

    if (addr && addr->sa_family == AF_UNIX) {
        struct sockaddr_un *un = (struct sockaddr_un *)addr;
        fprintf(stderr, "[DEBUG_LOG] connect(AF_UNIX, \"%s\")\n", un->sun_path[0] ? un->sun_path : un->sun_path + 1);
    }
    return orig(sockfd, addr, addrlen);
}

// 5. Hook getdents64 for /proc (keep hiding PIDs as it was partially successful)
//
// WHAT IT DOES: Hides all processes except init (PID 1) and ourselves when reading /proc
// WHY: Applications might enumerate /proc to count processes owned by different users.
// By hiding other processes, we make the system appear to have only one active user.
// Previous hooks (hook4/hook5) showed this approach had partial success.
// HOW IT WORKS:
//   1. Intercepts getdents64() which reads directory entries
//   2. Uses readlink on /proc/self/fd/N to check if we're reading from /proc
//   3. If yes, filters the returned directory entries (struct dirent64 array)
//   4. Removes entries with numeric names (PIDs) except PID 1 and our own PID
//   5. Uses memmove() to compact the buffer and adjusts the returned byte count
typedef ssize_t (*orig_getdents64_t)(int, void *, size_t);
ssize_t getdents64(int fd, void *buf, size_t len) {
    static orig_getdents64_t orig = NULL;
    if (!orig) orig = (orig_getdents64_t)dlsym(RTLD_NEXT, "getdents64");

    ssize_t nread = orig(fd, buf, len);
    if (nread <= 0) return nread;

    char path[PATH_MAX];
    char fd_path[64];
    snprintf(fd_path, sizeof(fd_path), "/proc/self/fd/%d", fd);
    ssize_t path_len = readlink(fd_path, path, sizeof(path) - 1);
    
    int is_proc = 0;
    if (path_len != -1) {
        path[path_len] = '\0';
        if (strcmp(path, "/proc") == 0) is_proc = 1;
    }

    if (!is_proc) return nread;

    int bpos = 0;
    pid_t my_pid = getpid();

    while (bpos < nread) {
        struct dirent64 *d = (struct dirent64 *)((char *)buf + bpos);
        if (isdigit(d->d_name[0])) {
            pid_t p = atoi(d->d_name);
            if (p != my_pid && p != 1) {
                memmove(d, (char *)d + d->d_reclen, nread - (bpos + d->d_reclen));
                nread -= d->d_reclen;
                continue;
            }
        }
        bpos += d->d_reclen;
    }
    return nread;
}
