# last build status
[![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient/)

# how to install

```shell
dnf copr enable vorona/aws-rpm-packages -y
dnf install workspacesclient -y
```

# notes

## tailing logs

```shell
tail ~/.local/share/Amazon\ Web\ Services/Amazon\ WorkSpaces/logs/{,pcoip/,WSP/}* -n 0 -f
```

## libcurl issue

```shell
% ldd libpcoip_core.so 
ldd: warning: you do not have execution permission for `./libpcoip_core.so'
./libpcoip_core.so: /lib64/libcurl.so.4: no version information available (required by ./libpcoip_core.so)
	linux-vdso.so.1 (0x00007fffc81d0000)
	libcurl.so.4 => /lib64/libcurl.so.4 (0x00007f584b0d5000)
```
## libPcoipCoreWrapper issue
```shell
% chrpath -l libPcoipCoreWrapper.so 
libPcoipCoreWrapper.so: no rpath or runpath tag found.
```