%define debug_package %{nil}
%define _build_id_links none
%undefine _auto_set_build_flags

BuildArch:     x86_64
Name:          workspacesclient
Version:       4.1.0.1523
Release:       3
License:       ASL 2.0
Group:         Converted/misc
Summary:       Amazon WorkSpaces Client for Ubuntu 18.04
Source0:       https://d3nt0h4h6pmmc4.cloudfront.net/ubuntu/dists/bionic/main/binary-amd64/workspacesclient_%{version}_amd64.deb

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
       ./opt/workspacesclient/System.IO.Compression.Native.so \
       ./opt/workspacesclient/System.Net.Http.Native.so \
       ./opt/workspacesclient/System.Net.Security.Native.so \
       ./opt/workspacesclient/libcoreclrtraceptprovider.so \
       ./opt/workspacesclient/libdbgshim.so \
       ./opt/workspacesclient/libmscordaccore.so \
       ./opt/workspacesclient/libmscordbi.so
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
rm -rf opt/workspacesclient/createdump

%install
mv opt %{buildroot}/

%__install -Dpm 0644 usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so \
        %{buildroot}/usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so
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

/usr/lib/x86_64-linux-gnu/pcoip-client/vchan_plugins/libvchan-plugin-clipboard.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/com.amazon.workspaces.svg

%license /opt/%{name}/Licenses/PCoIP/pcoip-linux-version-license.txt
%license /opt/%{name}/Licenses/third-party-license.txt
%doc /opt/%{name}/SOS_README.md


%changelog
* Sat Jul 30 2022 Anatolii Vorona 4.1.0.1523-3
- rebuild workspacesclient_amd64.deb
- remove createdump and its dependencies
