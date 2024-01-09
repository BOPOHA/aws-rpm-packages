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
/usr/lib/x86_64-linux-gnu/workspacesclient/dcv$ ldd * 2>&1 | grep "not found" -B10
dcvclient:
	not a dynamic executable
dcvclientbin:
	linux-vdso.so.1 (0x00007ffc711bf000)
	libdcv.so => not found
--
	libgobject-2.0.so.0 => /lib64/libgobject-2.0.so.0 (0x00007fddee132000)
	libglib-2.0.so.0 => /lib64/libglib-2.0.so.0 (0x00007fddecae0000)
	libgstapp-1.0.so.0 => /lib64/libgstapp-1.0.so.0 (0x00007fddee11d000)
	libgstbase-1.0.so.0 => /lib64/libgstbase-1.0.so.0 (0x00007fddeca5c000)
	libgstreamer-1.0.so.0 => /lib64/libgstreamer-1.0.so.0 (0x00007fddec90c000)
	libgstaudio-1.0.so.0 => /lib64/libgstaudio-1.0.so.0 (0x00007fddec88c000)
	libavcodec.so.60 => /lib64/libavcodec.so.60 (0x00007fddeb600000)
	libavutil.so.58 => /lib64/libavutil.so.58 (0x00007fddea400000)
	liblz4.so.1 => /lib64/liblz4.so.1 (0x00007fddee0f9000)
	libsoup-3.0.so.0 => /lib64/libsoup-3.0.so.0 (0x00007fddec7ef000)
	libturbojpeg.so.0 => not found
	libpcsclite.so.1 => /lib64/libpcsclite.so.1 (0x00007fddee0eb000)
	libprotobuf-c.so.1 => /lib64/libprotobuf-c.so.1 (0x00007fddec7e4000)
	libjson-glib-1.0.so.0 => /lib64/libjson-glib-1.0.so.0 (0x00007fddec7b8000)
	libGL.so.1 => /lib64/libGL.so.1 (0x00007fddeb579000)
	libsasl2.so.3 => /lib64/libsasl2.so.3 (0x00007fddeb55a000)
	libm.so.6 => /lib64/libm.so.6 (0x00007fddea31f000)
	libdcvwebauthnredirection.so => not found
--
	libsystemd.so.0 => /lib64/libsystemd.so.0 (0x00007f958499e000)
	libbrotlicommon.so.1 => /lib64/libbrotlicommon.so.1 (0x00007f958497b000)
	libcap.so.2 => /lib64/libcap.so.2 (0x00007f9584971000)
	liblz4.so.1 => /lib64/liblz4.so.1 (0x00007f958494f000)
	libzstd.so.1 => /lib64/libzstd.so.1 (0x00007f9584891000)
	libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00007f958486d000)
libharfbuzz-icu.so.0:
ldd: warning: you do not have execution permission for `./libharfbuzz-icu.so.0'
	linux-vdso.so.1 (0x00007ffe545af000)
	libharfbuzz.so.0 => /lib64/libharfbuzz.so.0 (0x00007f3379d77000)
	libicuuc.so.70 => not found
--
	libunistring.so.5 => /lib64/libunistring.so.5 (0x00007f71cd384000)
	libidn2.so.0 => /lib64/libidn2.so.0 (0x00007f71cd362000)
	libbrotlicommon.so.1 => /lib64/libbrotlicommon.so.1 (0x00007f71cd33f000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f71cdf18000)
	libblkid.so.1 => /lib64/libblkid.so.1 (0x00007f71cd301000)
libtiff.so.6:
ldd: warning: you do not have execution permission for `./libtiff.so.6'
	linux-vdso.so.1 (0x00007ffdb43f8000)
	libwebp.so.7 => /lib64/libwebp.so.7 (0x00007f611ee41000)
	liblzma.so.5 => /lib64/liblzma.so.5 (0x00007f611ee0e000)
	libjbig.so.0 => not found
```
## sh*t 02
```shell
strace -f -s 5120  workspacesclient > /tmp/log 2>&1

[pid 74161] <... read resumed>"/usr/lib/x86_64-linux-gnu/workspacesclient/dcv/dcvclient: line 18: 74427 Aborted                 (core dumped) \"${dcvclient_bin}\" \"$@\"\n", 8192) = 135
```