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

```shell
# vi /usr/lib/x86_64-linux-gnu/workspacesclient/dcv/dcvclient
echo "$@" >> /tmp/log1
:x
```
```shell
/usr/lib/x86_64-linux-gnu/workspacesclient/dcv/dcvclient --log-level info --disable-prompt-reconnect --disable-quic-probe --connection-block-retry-attempts 30 --standalone --auth-token eyJoaWdobGFuZGVyUENBQ2VydCI6IiIsImhpZ2hsYW5kZXJQQ0FDUkwiOiIiLCJrZXlCbG9iIjoiZW1Rd0xreHhHd0toTnQwQjFqSEZ2YnZIMVI4U3gzYXZtNWgwZTJkbWVUcFYycnFvU3BvVDFoL3ZuUFJ2Nkpnb1lrVUwvVjh0TTlXSzdYVkYvU200VVkxdVpiT2o2c2JtOTc0dXFwT2tCTFEveElkZUVuS1I3YkI2SlBMYitwM0VvOStkUHlmVEZNS09tcnE5dFQxZmRtQTFnOGh6Zm9EZXQ0akNhZDdsWkh5QlpwUmdEZTV0emwzRHh6aFRJaUhkYWxrdGszQ2J0T2hNOGx1aHR3bVZaRElNL1BQZHVqaTBWMEFhV2lQb2YveUUyRWl1eEFhWDg1cTdVcVpQRnE5bGVjdGdMYVBFNXpocjhOc0xMRkt1Q0VNOFovcjlXU0ovWklFTkRVQ3pId3RRQ3c5NUlrVThwbk5Pc29DWml3c3hMNG80dFhjTzV2ZXNGVDRMM1E3NW5RPT0iLCJjcmVkQmxvYiI6ImQ1alI5WVRBT3pwQS90Rlh0b0ZaVzBJMU4yWHBKVzVoWmlYelFsYkoxRUlsOUpGL0ZrNndGZ08rSlYvTExhWmZqZXgwMW1keHhQcm9uWXpuNit5R0xGVTlhVlVxYnUwTHVKb0ZPVlhqYWR5RzJRZEc5S2ZTTlZoTUNQNUVhYlZkN2ZKYWVjdE9Ta1g3WktIeGtCS2ExZz09In0= dcv://4a8089d0-993f-11ec-8602-064a2aad87df-3.prod.us-west-2.highlander.aws.a2z.com:4195?gatewayToken=7563e502-bb01-4902-80ed-fd994e3735f1#prod-us-west-2-02002f87-9c38-4801-8821-a1484cd9580c --transport websocket
Gtk-Message: 01:45:25.226: Failed to load module "canberra-gtk-module"
Gtk-Message: 01:45:25.226: Failed to load module "pk-gtk-module"
Gtk-Message: 01:45:25.227: Failed to load module "canberra-gtk-module"
Gtk-Message: 01:45:25.227: Failed to load module "pk-gtk-module"
2024-01-10 00:45:25,228600 [ 79637:79637 ] INFO  application - Starting DCV viewer version 2023.1 (r0) - 97ad23db840efdc5f8c3bf92fe1b6f98b077a1b1
2024-01-10 00:45:25,228779 [ 79637:79637 ] INFO  application - No metrics reporter available, metrics will be ignored
2024-01-10 00:45:25,228868 [ 79637:79637 ] INFO  application - Starting up application
2024-01-10 00:45:25,229219 [ 79637:79637 ] INFO  application - Loaded CSS
2024-01-10 00:45:25,234049 [ 79637:79637 ] INFO  certificate-store - Known hosts file: ~/.local/share/NICE/dcvclient/known_hosts.json
2024-01-10 00:45:25,234090 [ 79637:79637 ] INFO  certificate-store - Known hosts file does not exist yet
2024-01-10 00:45:25,234106 [ 79637:79637 ] INFO  certificates - Initializing root certificates
2024-01-10 00:45:25,234176 [ 79637:79637 ] INFO  system-resource-monitor - Start monitoring system resources
Fontconfig error: Cannot load default config file: No such file: (null)
2024-01-10 00:45:25,268381 [ 79637:79637 ] WARN  Gtk - Could not load a pixbuf from /org/gtk/libgtk/icons/16x16/status/open-menu-symbolic.symbolic.png.
This may indicate that pixbuf loaders or the mime database could not be found.
2024-01-10 00:45:25,268587 [ 79637:79637 ] INFO  stderr - **
Gtk:ERROR:../gtk/gtkiconhelper.c:495:ensure_surface_for_gicon: assertion failed (error == NULL): Failed to load /org/gtk/libgtk/icons/16x16/status/image-missing.png: Unrecognized image file format (gdk-pixbuf-error-quark, 3)

Bail out! Gtk:ERROR:../gtk/gtkiconhelper.c:495:ensure_surface_for_gicon: assertion failed (error == NULL): Failed to load /org/gtk/libgtk/icons/16x16/status/image-missing.png: Unrecognized image file format (gdk-pixbuf-error-quark, 3)
/usr/lib/x86_64-linux-gnu/workspacesclient/dcv/dcvclient: line 23: 79637 Aborted                 (core dumped) "${dcvclient_bin}" "$@"

```