%define _build_id_links none
%define app_name workspacesclient
%define app_libs_dir /usr/lib/x86_64-linux-gnu/%{app_name}

BuildArch:     x86_64
Name:          workspacesclient-wsp
Version:       2023.2.4580
Release:       7
License:       Freely redistributable without restriction
Group:         Converted/misc
Summary:       Amazon WorkSpaces Client for Ubuntu 22.04
Source0:       https://d3nt0h4h6pmmc4.cloudfront.net/new_workspacesclient_jammy_amd64.deb
Source1:       checksums.sha256

Conflicts:     %{name}-wsp
BuildRequires: systemd-rpm-macros
Requires:      /usr/bin/lsb_release
Requires:      gtk-update-icon-cache, glib2, shared-mime-info

%description
%{summary}
converted from DEB package,
that was "generated from Rust crate WorkSpacesClient"

%prep
(cd %{_sourcedir} && sha256sum -c %{SOURCE1})
%setup -cT
ar p %{SOURCE0} data.tar.xz | tar -xJ

%install
mkdir -p %{buildroot}/%{app_libs_dir}/dcv %{buildroot}/%{_libdir}

mv usr/bin %{buildroot}/usr/
mv usr/share %{buildroot}/usr/

%__install .%{app_libs_dir}/dcv/dcvclient                    %{buildroot}/%{app_libs_dir}/dcv/dcvclient
%__install .%{app_libs_dir}/dcv/dcvclientbin                 %{buildroot}/%{app_libs_dir}/dcv/dcvclientbin
%__install .%{app_libs_dir}/dcv/libdcv.so                    %{buildroot}/%{_libdir}/libdcv.so
%__install .%{app_libs_dir}/dcv/libdcvwebauthnredirection.so %{buildroot}/%{_libdir}/libdcvwebauthnredirection.so

%post
# nothing is here

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

if [ $1 -eq 0 ] ; then
  /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :

%clean

%files
%defattr(0644, root, root, 0755)
%attr(0755, root, root) %{_bindir}/%{app_name}
%attr(0755, root, root) %{app_libs_dir}/dcv/dcvclient
%attr(0755, root, root) %{app_libs_dir}/dcv/dcvclientbin
%attr(0755, root, root) %{_libdir}/libdcv.so
%attr(0755, root, root) %{_libdir}/libdcvwebauthnredirection.so

%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/com.amazon.workspacesclient.dcv.gschema.xml
%{_datadir}/glib-2.0/schemas/com.amazon.workspacesclient.gschema.xml
%{_datadir}/icons/hicolor/*
%lang(de) %{_datadir}/locale/de_DE/
%lang(es) %{_datadir}/locale/es/
%lang(fr) %{_datadir}/locale/fr/
%lang(ja) %{_datadir}/locale/ja/
%lang(ko) %{_datadir}/locale/ko/
%lang(pt) %{_datadir}/locale/pt_BR/
%lang(zh) %{_datadir}/locale/zh_CN/

%license %{_datadir}/doc/%{app_name}/copyright

%changelog
* Thu Jan 11 2024 Anatolii Vorona 2023.2.4580-7
- spec refactoring, cleaning, polishing

* Thu Jan 11 2024 Anatolii Vorona 2023.2.4580-6
- remove unused libs
- replace gstreamer-1.0 with system libs
- remove all the rest libs....

* Wed Jan 10 2024 Anatolii Vorona 2023.2.4580-5
- replace gdk-pixbuf-2.0/gtk-3.0 with system libs
- first working version...

* Tue Jan 9 2024 Anatolii Vorona 2023.2.4580-4
- patched rpath and shared lib names for some libs
- still WIP

* Thu Dec 28 2023 Anatolii Vorona 2023.2.4580-1
- bump version

* Sun Dec 10 2023 Anatolii Vorona 2023.1.4537-1
- first rebuild new_workspacesclient_jammy_amd64.deb
