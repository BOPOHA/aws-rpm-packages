# AWS VPN Client RPM

[![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/)

This package repackages the official AWS VPN Client Debian package for Fedora.

Starting with AWS VPN Client 6.x, the application has a new architecture: the
graphical interface is an Electron application, accompanied by a native daemon,
CLI, and posture agent. The upstream Debian package is now largely suitable for
direct repackaging, so the RPM does not patch or reverse-engineer application
files. It only translates Debian integration details such as paths, permissions,
dependencies, and service lifecycle handling to their RPM/Fedora equivalents.

## Installation

```shell
sudo dnf copr enable vorona/aws-rpm-packages
sudo dnf install awsvpnclient
```

The package enables and starts `aws-client-vpn-daemon.service`. The graphical
client can be launched from the desktop menu, and the CLI is available as
`aws-vpn-client`.

## Building locally

Install the RPM packaging tools, then run:

```shell
cd awsvpnclient
make rpmbuild
```

The resulting RPM is written under `~/rpmbuild/RPMS/x86_64/`. The build uses the
official upstream Debian package as its only source and installs its application
payload under `/opt/awsvpnclient` without modifying it.

## Service and logs

```shell
systemctl status aws-client-vpn-daemon.service
journalctl -u aws-client-vpn-daemon.service
```

The client and DNS helper may also write logs below `/var/log/awsvpnclient`.

The DNS integration uses `systemd-resolved` through `resolvectl`. Confirm that
the service is active if VPN DNS resolution does not work:

```shell
systemctl status systemd-resolved.service
resolvectl status
```

## Support status

AWS officially supports the distributed Debian/Ubuntu package, not this Fedora
repackaging. Report RPM packaging problems in this repository; application
problems may need to be reproduced with the official package before contacting
AWS Support.

## Alternatives

- [openlawsvpn](https://github.com/JonathanxD/openaws-vpn-client)
- [samm-git/aws-vpn-client](https://github.com/samm-git/aws-vpn-client)
- [awsvpnclient-nix](https://github.com/AddG0/awsvpnclient-nix)
- [awsvpn-flake](https://github.com/Tebro/awsvpn-flake)
- [AUR awsvpnclient](https://aur.archlinux.org/packages/awsvpnclient)

The latest official version and installation documentation are available in the
[AWS Client VPN documentation](https://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-connect-linux.html).
