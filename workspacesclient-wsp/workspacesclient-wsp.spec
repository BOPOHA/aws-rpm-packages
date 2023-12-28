%define _build_id_links none
%define app_name workspacesclient
%define app_libs_dir /usr/lib/x86_64-linux-gnu/%{app_name}

%global __provides_exclude_from  %{app_libs_dir}
%global __requires_exclude_from  %{app_libs_dir}

BuildArch:     x86_64
Name:          workspacesclient-wsp
Version:       2023.2.4580
Release:       1
License:       Freely redistributable without restriction
Group:         Converted/misc
Summary:       Amazon WorkSpaces Client for Ubuntu 22.04
Source0:       https://d3nt0h4h6pmmc4.cloudfront.net/new_workspacesclient_jammy_amd64.deb
Source1:       checksums.sha256

Obsoletes:     %{app_name} <= 4.5.0.2006
#Requires:      libdeflate
#Requires:      jbigkit-libs
#Requires:      PackageKit-gtk3-module
#Requires:      libcanberra-gtk3
#Requires:      webkit2gtk4.0
BuildRequires: systemd-rpm-macros
Requires:      lsb_release

%description
%{summary}
converted from DEB package,
that was "generated from Rust crate WorkSpacesClient"

%prep
(cd %{_sourcedir} && sha256sum -c %{SOURCE1})
%setup -cT
ar p %{SOURCE0} data.tar.xz | tar -xJ

%install
mv usr %{buildroot}/
#rm %{buildroot}%{app_libs_dir}/dcv/libharfbuzz-icu.so.0
#ln -s ../../../../..%{_libdir}/libharfbuzz-icu.so.0 %{buildroot}%{app_libs_dir}/dcv/libharfbuzz-icu.so.0
#ln -s ../../../../..%{_libdir}/libjbig.so.2.1       %{buildroot}%{app_libs_dir}/dcv/libjbig.so.0

%clean

%files
%defattr(0644, root, root, 0755)
%attr(0755, root, root) %{_bindir}/%{app_name}
%attr(0755, root, root) %{app_libs_dir}/dcv/dcvclient
%attr(0755, root, root) %{app_libs_dir}/dcv/dcvclientbin
%attr(0755, root, root) %{app_libs_dir}/dcv/gdk-pixbuf-query-loaders
%attr(0755, root, root) %{app_libs_dir}/dcv/gst-plugin-scanner
%attr(0755, root, root) %{app_libs_dir}/dcv/gtk-query-immodules-3.0

%{app_libs_dir}/dcv/gstreamer-1.0/*.so
%{app_libs_dir}/dcv/gdk-pixbuf-2.0/2.10.0/loaders/*.so
%{app_libs_dir}/dcv/gtk-3.0/3.0.0/immodules/*.so
%{app_libs_dir}/dcv/gio/modules/libgioopenssl.so
%{app_libs_dir}/dcv/sasl2/*.so
%{app_libs_dir}/dcv/*.so{,.*}

%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/com.amazon.workspacesclient.dcv.gschema.xml
%{_datadir}/glib-2.0/schemas/com.amazon.workspacesclient.gschema.xml
%{_datadir}/icons/hicolor/*
%{_datadir}/locale/*

%license %{_datadir}/doc/%{app_name}/copyright

%changelog
* Thu Dec 28 2023 Anatolii Vorona 2023.2.4580-1
- bump version

* Sun Dec 10 2023 Anatolii Vorona 2023.1.4537-1
- first rebuild new_workspacesclient_jammy_amd64.deb
