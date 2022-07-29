%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}
%define _build_id_links none
%undefine _auto_set_build_flags


BuildArch:     x86_64
Name:          awsvpnclient
Version:       3.1.0
Release:       2
License:       Apache
Group:         Converted/misc
Summary:       AWS VPN Client for Ubuntu 18.04
Source0:       https://d20adtppz83p9s.cloudfront.net/GTK/%{version}/awsvpnclient_amd64.deb
Source1:       70-awsvpnclient.preset

BuildRequires: systemd-rpm-macros

%description
%{summary}

%prep
%setup -cT
ar p %{SOURCE0} data.tar.xz | tar -xJ

find . -iname "*.a" -delete
find . -iname "*.pdb" -delete
find . -iname "*.json" -delete
mv ./opt/%{name}/Service/Resources/openvpn       ./opt/%{name}/Resources/
mv ./opt/%{name}/Service/ACVC.GTK.Service{,.dll} ./opt/%{name}/
rm -rf ./opt/%{name}/Service
rm -rf ./opt/%{name}/SQLite.Interop.dll # https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=awsvpnclient#n31
                                        # Workaround for missing compatibility of the SQL library with arch linux:
                                        # Intentionally break the metrics agent,
                                        # it will be unable to laod the dynamic lib and wont start but continue with error message
                                        # fixes errors:
                                        # gtk_tree_model_iter_nth_child: assertion 'n >= 0' failed
                                        # gtk_list_store_get_path: assertion 'iter->stamp == priv->stamp' failed
sed -i "s#Service/ACVC.GTK.Service#ACVC.GTK.Service#;" ./etc/systemd/system/%{name}.service

rm -rf \
       ./opt/%{name}/libdbgshim.so \
       ./opt/%{name}/libmscordaccore.so \
       ./opt/%{name}/libmscordbi.so \
       ./opt/%{name}/System.IO.Compression.Native.so \
       ./opt/%{name}/System.Net.Http.Native.so \
       ./opt/%{name}/System.Net.Security.Native.so \
       ./opt/%{name}/createdump

%install
mv opt %{buildroot}/
mv usr %{buildroot}/
%__install -D etc/systemd/system/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
%__install -D %{SOURCE1} %{buildroot}%{_presetdir}/70-%{name}.preset

%__install -d %{buildroot}/opt/%{name}/Service/Resources/openvpn
ln -s ../../../Resources/openvpn/configure-dns %{buildroot}/opt/%{name}/Service/Resources/openvpn/configure-dns

%clean

%files
%defattr(0644, root, root, 0755)
%attr(0755, root, root) "/opt/%{name}/AWS VPN Client"
%attr(0755, root, root) /opt/%{name}/Resources/openvpn/acvc-openvpn
%attr(0755, root, root) /opt/%{name}/Resources/openvpn/configure-dns
%attr(0755, root, root) /opt/%{name}/ACVC.GTK.Service
/opt/%{name}/*.dll
/opt/%{name}/*/*.dll
/opt/%{name}/*.so
/opt/%{name}/Resources/acvc-64.png

/usr/share/applications/%{name}.desktop
/usr/share/pixmaps/acvc-64.png
%{_presetdir}/70-%{name}.preset
%{_unitdir}/%{name}.service

/opt/%{name}/Service/Resources/openvpn/configure-dns

%license /opt/%{name}/Resources/LINUX-LICENSE.txt
%license /opt/%{name}/Resources/THIRD-PARTY-LICENSES-GTK.txt
%doc /opt/%{name}/SOS_README.md
%doc /usr/share/doc/%{name}
%dir /opt/%{name}/
%dir /opt/%{name}/Resources/
%dir /opt/%{name}/Resources/openvpn
%dir /opt/%{name}/Service/
%dir /opt/%{name}/Service/Resources
%dir /opt/%{name}/Service/Resources/openvpn
%dir /opt/%{name}/de/
%dir /opt/%{name}/es/
%dir /opt/%{name}/fr/
%dir /opt/%{name}/it/
%dir /opt/%{name}/ja/
%dir /opt/%{name}/ko/
%dir /opt/%{name}/pt-BR/
%dir /opt/%{name}/zh-Hans/
%dir /opt/%{name}/zh-Hant/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Tue Jul 26 2022 Anatolii Vorona  3.1.0-15
- rebuild awsvpnclient_amd64.deb
- remove unused files
- remove createdump and its dependencies
