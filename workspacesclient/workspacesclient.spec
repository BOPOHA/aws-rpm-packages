%define debug_package %{nil}
%define libcurl_version 7.68.0
%define _build_id_links none
%undefine _auto_set_build_flags

%global __provides_exclude_from  ^(/opt/workspacesclient/.*\\.so|/usr/lib/x86_64-linux-gnu/pcoip-client/.*)$
%global __requires_exclude_from  ^(/opt/workspacesclient/.*\\.so|/usr/lib/x86_64-linux-gnu/pcoip-client/.*)$

BuildArch:     x86_64
Name:          workspacesclient
Version:       4.7.0.4312
Release:       4
License:       Freely redistributable without restriction
Group:         Converted/misc
Summary:       Amazon WorkSpaces Client for Ubuntu 20.04
Source0:       https://d3nt0h4h6pmmc4.cloudfront.net/ubuntu/dists/focal/main/binary-amd64/workspacesclient_%{version}_amd64.deb
Source1:       https://mirror.us.leaseweb.net/ubuntu/pool/universe/h/hiredis/libhiredis0.14_0.14.0-6_amd64.deb
Source2:       https://curl.haxx.se/download/curl-%{libcurl_version}.tar.gz

Requires:      openssl1.1
Requires:      webkit2gtk4.0
Requires:      bzip2-libs
BuildRequires: patchelf
BuildRequires: systemd-rpm-macros

Conflicts:     %{name}-wsp

%description
%{summary}

%prep
%setup -cT
ar p %{SOURCE0} data.tar.xz | tar -xJ
find . -iname "*.pdb" -delete
rm -rf \
       ./opt/%{name}/workspacesclient.deps.json \
       ./opt/%{name}/workspacesclient.runtimeconfig.json \

# remove unused trackers
rm -rf \
       ./opt/%{name}/libmscordbi.so \
       ./opt/%{name}/libmscordaccore.so \
       ./opt/%{name}/libcoreclrtraceptprovider.so \
       ./opt/%{name}/createdump

# W: files-duplicate
rm -rf \
       ./opt/%{name}/libavcodec.so.58 \
       ./opt/%{name}/libavcodec.so.58.134.100 \
       ./opt/%{name}/libavdevice.so.58 \
       ./opt/%{name}/libavdevice.so.58.13.100 \
       ./opt/%{name}/libavfilter.so.7 \
       ./opt/%{name}/libavfilter.so.7.110.100 \
       ./opt/%{name}/libavformat.so.58 \
       ./opt/%{name}/libavformat.so.58.76.100 \
       ./opt/%{name}/libavutil.so.56 \
       ./opt/%{name}/libavutil.so.56.70.100 \
       ./opt/%{name}/libswresample.so.3 \
       ./opt/%{name}/libswresample.so.3.9.100 \
       ./opt/%{name}/libswscale.so.5 \
       ./opt/%{name}/libswscale.so.5.9.100 \
       ./opt/%{name}/libwolfssl.so.35.2.1
mv ./opt/%{name}/libwolfssl.so{.35,}

patchelf --set-rpath '$ORIGIN' --force-rpath                          ./opt/%{name}/libPcoipCoreWrapper.so
patchelf --set-rpath '$ORIGIN:/usr/lib/x86_64-linux-gnu/pcoip-client' ./opt/%{name}/libpcoip_core.so
patchelf --replace-needed libwolfssl.so.35 libwolfssl.so              ./opt/%{name}/libPcoipCoreWrapper.so
patchelf --replace-needed libwolfssl.so.35 libwolfssl.so              ./opt/%{name}/libpcoip_core.so
patchelf --replace-needed libcurl.so.4.6.0 libcurl.so                 ./opt/%{name}/libpcoip_core.so
patchelf --replace-needed libbz2.so.1.0    libbz2.so.1                ./opt/%{name}/libavformat.so

ar p %{SOURCE1} data.tar.xz | tar -xJ

%setup -a 2 -T -D

%build
cd %{_builddir}/curl-%{libcurl_version}
CC=clang ./configure --with-ssl --enable-versioned-symbols --enable-harden
make
ldd lib/.libs/libcurl.so.4.6.0

%install
mv opt %{buildroot}/

%__install -Dpm 0644 usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so \
        %{buildroot}/usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so
%__install -Dpm 0644 usr/lib/x86_64-linux-gnu/libhiredis.so.0.14 %{buildroot}/usr/lib/x86_64-linux-gnu/pcoip-client/libhiredis.so.0.14
%__install -Dpm 0644 usr/share/applications/%{name}.desktop      %{buildroot}%{_datadir}/applications/%{name}.desktop
%__install -Dpm 0644 usr/share/pixmaps/com.amazon.workspaces.svg %{buildroot}%{_datadir}/pixmaps/com.amazon.workspaces.svg
%__install -Dpm 0644 %{_builddir}/curl-%{libcurl_version}/lib/.libs/libcurl.so.4.6.0 \
                                                                 %{buildroot}/opt/%{name}/libcurl.so

%clean

%files
%defattr(0644, root, root, 0755)
%attr(0755, root, root) /opt/%{name}/%{name}
/opt/%{name}/*.dll
/opt/%{name}/*.so
/opt/%{name}/appsettings.json
/opt/%{name}/Assets/*

/usr/lib/x86_64-linux-gnu/pcoip-client/libhiredis.so.0.14
/usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/com.amazon.workspaces.svg

%license /opt/%{name}/Licenses/PCoIP/pcoip-linux-version-license.txt
%license /opt/%{name}/Licenses/third-party-license.txt
%dir /opt/%{name}/
%dir /opt/%{name}/Licenses
%dir /opt/%{name}/Licenses/PCoIP
%dir /opt/%{name}/Assets


%changelog
* Sat Dec 30 2023 Anatolii Vorona 4.7.0.4312-4
- builded own libcurl.so instead of portintg chain of Ubuntu 20.04 libs
- patched rpath and shared lib names for some libs
- works fine on fc39

* Thu Dec 28 2023 Anatolii Vorona 4.7.0.4312-1
- bump version

* Thu Dec 29 2022 Anatolii Vorona 4.5.0.2006
- Resolved the issue of users being unable to disconnect from WorkSpaces when their network connectivity was lost or unavailable.
- Updated PCoIP SDK for the WorkSpaces Linux client.

* Tue Nov 8 2022 Anatolii Vorona 4.4.0.1808
- move from bionic to focal binaries

* Mon Nov 7 2022 Anatolii Vorona 4.3.0.1766
- Updated PCoIP SDK for Linux.
- Fixed changing monitor's relative positions issue on WorkSpaces.
- Minor bug fixes and enhancements.

* Sat Jul 30 2022 Anatolii Vorona 4.1.0.1523-3
- rebuild workspacesclient_amd64.deb
- remove createdump and its dependencies
- remove liblttng-ust.so.0 dependency
