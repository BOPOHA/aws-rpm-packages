# last build status
[![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient-wsp/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient-wsp/)

# how to install

```shell
dnf copr enable vorona/aws-rpm-packages -y
dnf install workspacesclient-wsp -y
```
# Debugging
## sh*t 01
temporary solution while debugging
```shell
LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/workspacesclient/dcv workspacesclient
LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/workspacesclient/dcv strace workspacesclient 2>&1 | grep No\ s -A1

PATH=
```
## sh*t 02
maybe something of these things we have to add to the rpm spec

```shell
#!/bin/sh
set -e

case "$1" in
    configure)
        touch --no-create /usr/share/icons/hicolor || :
        touch --no-create /usr/share/mime/packages || :

        update-desktop-database || :
        gtk-update-icon-cache /usr/share/icons/hicolor || :
        glib-compile-schemas /usr/share/glib-2.0/schemas || :
        update-mime-database /usr/share/mime &> /dev/null || :

        arch=$(arch)
        export LD_LIBRARY_PATH="/usr/lib/${arch}-linux-gnu/workspacesclient/dcv:$LD_LIBRARY_PATH"
        export PATH="/usr/lib/${arch}-linux-gnu/workspacesclient/dcv:$PATH"
        gdk-pixbuf-query-loaders /usr/lib/${arch}-linux-gnu/workspacesclient/dcv/gdk-pixbuf-2.0/2.10.0/loaders/*.so > /usr/lib/${arch}-linux-gnu/workspacesclient/dcv/gdk-pixbuf-2.0/2.10.0/loaders.cache
        gtk-query-immodules-3.0 /usr/lib/${arch}-linux-gnu/workspacesclient/dcv/gtk-3.0/3.0.0/immodules/*.so > /usr/lib/${arch}-linux-gnu/workspacesclient/dcv/gtk-3.0/3.0.0/immodules.cache

        # Hack in order to have dconf working
        ln -sf "/usr/lib/${arch}-linux-gnu/gio/modules/libdconfsettings.so" "/usr/lib/${arch}-linux-gnu/workspacesclient/dcv/gio/modules/"
    ;;

    abort-upgrade|abort-remove|abort-deconfigure)
    ;;

    *)
        echo "postinst called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
```

## sh*t 03
unincluded PCOIP module only wants to work on Ubuntu 20.04 )))
```text
[pid 25572] execve("/home/user/bin/lsb_release", ["lsb_release", "-r"], 0x5570514fc940 /* 73 vars */ <unfinished ...>
[pid 25551] <... openat resumed>)       = -1 ENOENT (No such file or directory)
[pid 25548] <... sendmsg resumed>)      = 48
[pid 25564] futex(0x7fc1dd3683e0, FUTEX_WAIT_BITSET_PRIVATE|FUTEX_CLOCK_REALTIME, 0, {tv_sec=1703726844, tv_nsec=333888292}, FUTEX_BITSET_MATCH_ANY <unfinished ...>
[pid 25551] openat(AT_FDCWD, "/usr/lib64/libGLX.so.1", O_RDONLY|O_CLOEXEC <unfinished ...>
[pid 25548] poll([{fd=19, events=POLLIN}, {fd=20, events=POLLIN}], 2, -1 <unfinished ...>
[pid 25551] <... openat resumed>)       = -1 ENOENT (No such file or directory)
[pid 25548] <... poll resumed>)         = 1 ([{fd=20, revents=POLLIN}])
[pid 25551] munmap(0x7fc1dc356000, 86051 <unfinished ...>
[pid 25548] read(20,  <unfinished ...>
[pid 25551] <... munmap resumed>)       = 0

[pid 25572] openat(AT_FDCWD, "/home/user/bin/lsb_release", O_RDONLY) = 3
[pid 25572] newfstatat(AT_FDCWD, "/home/user/bin/lsb_release", {st_mode=S_IFREG|0755, st_size=35, ...}, 0) = 0
[pid 25572] ioctl(3, TCGETS, 0x7ffeeba5e940) = -1 ENOTTY (Inappropriate ioctl for device)
[pid 25572] lseek(3, 0, SEEK_CUR)       = 0
[pid 25551] write(29, "\1\0\0\0\0\0\0\0", 8) = 8
[pid 25551] openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 34
[pid 25551] newfstatat(34, "",  <unfinished ...>
[pid 25536] futex(0x7fc1dd3683e4, FUTEX_WAKE_PRIVATE, 1 <unfinished ...>
[pid 25572] read(3,  <unfinished ...>
[pid 25551] <... newfstatat resumed>{st_mode=S_IFREG|0644, st_size=86051, ...}, AT_EMPTY_PATH) = 0
[pid 25572] <... read resumed>"#!/bin/bash\necho  \"Release:\t20.04\"\n", 80) = 35
[pid 25564] <... futex resumed>)        = 0
```