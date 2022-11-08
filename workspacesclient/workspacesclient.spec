%define debug_package %{nil}
%define _build_id_links none
%undefine _auto_set_build_flags

BuildArch:     x86_64
Name:          workspacesclient
Version:       4.3.0.1766
Release:       3
License:       Freely redistributable without restriction
Group:         Converted/misc
Summary:       Amazon WorkSpaces Client for Ubuntu 18.04
Source0:       https://d3nt0h4h6pmmc4.cloudfront.net/ubuntu/dists/bionic/main/binary-amd64/workspacesclient_%{version}_amd64.deb
Source1:       https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/x86_64/Packages/h/hiredis-0.13.3-17.fc35.x86_64.rpm

BuildRequires: systemd-rpm-macros

%description
%{summary}

%prep
%setup -cT
ar p %{SOURCE0} data.tar.xz | tar -xJ
find . -iname "*.a" -delete
find . -iname "*.pdb" -delete
rm -rf \
       ./opt/workspacesclient/workspacesclient.deps.json \
       ./opt/workspacesclient/workspacesclient.runtimeconfig.json
rm -rf \
       ./opt/%{name}/System.Net.Security.Native.so \
       ./opt/%{name}/System.Net.Http.Native.so \
       ./opt/%{name}/System.IO.Compression.Native.so \
       ./opt/%{name}/libmscordbi.so \
       ./opt/%{name}/libmscordaccore.so \
       ./opt/%{name}/libdbgshim.so \
       ./opt/%{name}/libcoreclrtraceptprovider.so \
       ./opt/%{name}/createdump
# and leave these libs:
#       ./opt/workspacesclient/libhostfxr.so \
#       ./opt/workspacesclient/libhostpolicy.so \
#       ./opt/workspacesclient/libcoreclr.so \
#       ./opt/workspacesclient/System.Globalization.Native.so \
#       ./opt/workspacesclient/System.Native.so \
#       ./opt/workspacesclient/libclrjit.so \
#       ./opt/workspacesclient/System.Security.Cryptography.Native.OpenSsl.so \
#       ./opt/workspacesclient/libpcoip_core.so
#       ./opt/workspacesclient/libPcoipCoreWrapper.so \
#rm -rf opt/workspacesclient/Assets/

rpm2cpio %{SOURCE1} | cpio -icdv ./usr/lib64/libhiredis.so.0.13

%install
mv opt %{buildroot}/

%__install -Dpm 0644 usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so \
        %{buildroot}/usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so
%__install -Dpm 0644 usr/lib64/libhiredis.so.0.13                %{buildroot}/usr/lib/x86_64-linux-gnu/pcoip-client/libhiredis.so.0.13
%__install -Dpm 0644 usr/share/applications/%{name}.desktop      %{buildroot}%{_datadir}/applications/%{name}.desktop
%__install -Dpm 0644 usr/share/pixmaps/com.amazon.workspaces.svg %{buildroot}%{_datadir}/pixmaps/com.amazon.workspaces.svg

%clean

%files
%defattr(0644, root, root, 0755)
%attr(0755, root, root) /opt/%{name}/%{name}
/opt/%{name}/*.dll
/opt/%{name}/*.so
/opt/%{name}/appsettings.json
/opt/%{name}/Assets/*

/usr/lib/x86_64-linux-gnu/pcoip-client/libhiredis.so.0.13
/usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/com.amazon.workspaces.svg

%license /opt/%{name}/Licenses/PCoIP/pcoip-linux-version-license.txt
%license /opt/%{name}/Licenses/third-party-license.txt
%doc /opt/%{name}/SOS_README.md
%dir /opt/%{name}/
%dir /opt/%{name}/Licenses
%dir /opt/%{name}/Licenses/PCoIP
%dir /opt/%{name}/Assets


%changelog
* Mon Nov 7 2022 Anatolii Vorona 4.3.0.1766
- Ubuntu Linux 20.04 support.
- Updated PCoIP SDK for Linux.
- Fixed changing monitor's relative positions issue on WorkSpaces.
- Minor bug fixes and enhancements.

* Sat Jul 30 2022 Anatolii Vorona 4.1.0.1523-3
- rebuild workspacesclient_amd64.deb
- remove createdump and its dependencies
- remove liblttng-ust.so.0 dependency
