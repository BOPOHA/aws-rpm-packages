# Disable stripping:
%define __spec_install_post /usr/lib/rpm/brp-compress || :

%define debug_package %{nil}
%define _build_id_links none
%undefine _auto_set_build_flags

%global __provides_exclude_from ^/opt/awsvpnclient/.*\\.so(\\.[0-9]+)*$
%global __requires_exclude_from ^/opt/awsvpnclient/.*\\.so(\\.[0-9]+)*$
%global __requires_exclude ^lib(crypto|ffmpeg|ssl)\\.so\\(\\)\\(64bit\\)$

ExclusiveArch: x86_64
Name:          awsvpnclient
Version:       6.2.0
Release:       1%{?dist}
License:       LicenseRef-Proprietary
Group:         Converted/misc
Summary:       AWS VPN Client
URL:           https://aws.amazon.com/vpn/
Source0:       https://d20adtppz83p9s.cloudfront.net/GTK/%{version}/awsvpnclient_amd64.deb

BuildRequires: binutils
BuildRequires: gzip
BuildRequires: systemd-rpm-macros
BuildRequires: tar
Requires:      alsa-lib
Requires:      gtk3
Requires:      libdrm
Requires:      libnotify
Requires:      libXScrnSaver
Requires:      libXtst
Requires:      mesa-libgbm
Requires:      nss
Requires:      systemd-resolved
Requires(pre): procps-ng
Requires(pre): systemd
Requires(post): systemd
Requires(preun): procps-ng
Requires(postun): systemd
Requires(posttrans): systemd

%description
%{summary}

%prep
%setup -cT
ar p %{SOURCE0} data.tar.gz | tar -z -x

%install
cp -a opt %{buildroot}/
install -Dpm 0644 etc/systemd/system/aws-client-vpn-daemon.service \
    %{buildroot}%{_unitdir}/aws-client-vpn-daemon.service
install -Dpm 0644 usr/share/applications/aws-vpn-client.desktop \
    %{buildroot}%{_datadir}/applications/aws-vpn-client.desktop
mkdir -p %{buildroot}%{_bindir}
ln -s /opt/%{name}/aws-vpn-client %{buildroot}%{_bindir}/aws-vpn-client
install -dm 0700 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 0755 %{buildroot}%{_presetdir}
printf 'enable aws-client-vpn-daemon.service\n' > \
    %{buildroot}%{_presetdir}/70-%{name}.preset

chmod 0750 %{buildroot}/opt/%{name}/aws-client-vpn-daemon
chmod 0755 %{buildroot}/opt/%{name}/aws-vpn-client
chmod 0755 %{buildroot}/opt/%{name}/aws-vpn-client-agent
chmod 0750 %{buildroot}/opt/%{name}/dns/configure-dns

%files
/opt/%{name}
%{_unitdir}/aws-client-vpn-daemon.service
%{_presetdir}/70-%{name}.preset
%{_bindir}/aws-vpn-client
%{_datadir}/applications/aws-vpn-client.desktop
%attr(0700,root,root) %dir %{_sharedstatedir}/%{name}

%pre
if [ "$1" -gt 1 ]; then
    # Stop both current and legacy processes before replacing their binaries.
    systemctl stop aws-client-vpn-daemon.service >/dev/null 2>&1 || :
    systemctl stop awsvpnclient.service >/dev/null 2>&1 || :
    systemctl disable awsvpnclient.service >/dev/null 2>&1 || :
    pkill -x "AWS VPN Client" >/dev/null 2>&1 || :
    pkill -x AWSVPNClient >/dev/null 2>&1 || :
    pkill -f aws-vpn-client-agent >/dev/null 2>&1 || :
fi

%post
%systemd_post aws-client-vpn-daemon.service

%preun
if [ "$1" -eq 0 ]; then
    pkill -x "AWS VPN Client" >/dev/null 2>&1 || :
    pkill -x AWSVPNClient >/dev/null 2>&1 || :
    pkill -f aws-vpn-client-agent >/dev/null 2>&1 || :
fi
%systemd_preun aws-client-vpn-daemon.service

%postun
%systemd_postun_with_restart aws-client-vpn-daemon.service
if [ "$1" -eq 0 ]; then
    systemctl reset-failed aws-client-vpn-daemon.service >/dev/null 2>&1 || :
fi

%posttrans
if [ -d /run/systemd/system ]; then
    systemctl preset aws-client-vpn-daemon.service >/dev/null 2>&1 || :
    systemctl start aws-client-vpn-daemon.service >/dev/null 2>&1 || :
fi

%changelog
* Sat Oct 03 2026 AV - 6.2.0-1
- repackage the new upstream Electron-based client without modifications
- translate upstream permissions, dependencies, and service lifecycle to RPM
- add systemd-resolved dependency and transaction-safe service migration

* Fri May 15 2026 AV - 5.3.2-3
- fix sqlite dep: require sqlite-libs instead of unversioned libsqlite3.so path (Fedora 44)

* Thu Mar 12 2026 AV - 5.3.2-2
- add hook build and preload override
- exclude .dll/.dylib auto-requires

* Thu Mar 5 2026 AV - 5.3.2-1
- bump version

* Tue Nov 4 2025 AV - 5.3.1-1
- bumb version

* Wed Apr 23 2025 AV - 5.2.0-1
- bumb version

* Wed Apr 23 2025 JO - 4.1.0-9
- Fixed conflict with /usr/sbin/ip on Fedora 42

* Sat Dec 21 2024 AV - 4.1.0-8
- added symlink for /usr/sbin/ip, because they have hash validation for at least configure-dns and acvc-openvpn

* Sat Nov 16 2024 AV - 4.1.0-7
- bumb version

* Thu Aug 1 2024 Cott Lang - 3.14.0-1
- Updated the OpenVPN and OpenSSL libraries.

* Mon May 27 2024 Anatolii Vorona - 3.13.0-1
- bump version
- Automatically reconnect when local area network ranges change.

* Mon Apr 29 2024 Cott Lang - 3.12.2-1
- bump version
- Resolved a SAML authentication issue with Chromium-based browsers since version 123.
- Improved security posture.
- Fixed connectivity issues for some LAN configurations.

* Sun Dec 10 2023 Anatolii Vorona - 3.11.0-1
- bump version
- improved accessibility

* Sat Aug 26 2023 Anatolii Vorona - 3.9.0-1
- bump version
- improved security posture
- fixed a connectivity issue when NAT64 is enabled in the client network
- minor bug fixes and enhancements
* Tue Mar 7 2023 Anatolii Vorona  3.4.0-1
- bump version
- disable Globalization. ICU is needed except if globalization is disabled
  Client works with libicu versions 67 and 69, and fc37 ships with libicu v71.

* Fri Jan 27 2023 Anatolii Vorona  3.2.0-1
- Added support for "verify-x509-name" OpenVPN flag.

* Tue Dec 13 2022 Anatolii Vorona  3.1.0-5
- configure-dns is working now

* Tue Jul 26 2022 Anatolii Vorona  3.1.0-2
- rebuild awsvpnclient_amd64.deb
- remove unused files
- remove createdump and its dependencies
