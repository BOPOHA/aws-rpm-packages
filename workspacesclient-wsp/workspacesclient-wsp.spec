%define _build_id_links none
%define app_name workspacesclient
%define app_libs_dir /usr/lib/x86_64-linux-gnu/%{app_name}

%global __provides_exclude_from  %{app_libs_dir}
%global __requires_exclude_from  %{app_libs_dir}

BuildArch:     x86_64
Name:          workspacesclient-wsp
Version:       2023.2.4580
Release:       6
License:       Freely redistributable without restriction
Group:         Converted/misc
Summary:       Amazon WorkSpaces Client for Ubuntu 22.04
Source0:       https://d3nt0h4h6pmmc4.cloudfront.net/new_workspacesclient_jammy_amd64.deb
Source1:       checksums.sha256
#Source2:       http://archive.ubuntu.com/ubuntu/pool/main/j/jbigkit/libjbig0_2.1-3.1ubuntu0.22.04.1_amd64.deb
#Source3:       http://archive.ubuntu.com/ubuntu/pool/main/i/icu/libicu70_70.1-2ubuntu1_amd64.deb

Conflicts:     %{name}-wsp
#Requires:      libdeflate
Requires:      jbigkit-libs
Requires:      harfbuzz-icu
#Requires:      PackageKit-gtk3-module
#Requires:      libcanberra-gtk3
#Requires:      webkit2gtk4.0
#Requires:      libicu71
BuildRequires: systemd-rpm-macros
BuildRequires: patchelf
Requires:      /usr/bin/lsb_release
Requires:      gtk-update-icon-cache
Requires:      glib2
Requires:      shared-mime-info
Requires:      gdk-pixbuf2, gtk3, gstreamer1

%description
%{summary}
converted from DEB package,
that was "generated from Rust crate WorkSpacesClient"

%prep
(cd %{_sourcedir} && sha256sum -c %{SOURCE1})
%setup -cT
ar p %{SOURCE0} data.tar.xz | tar -xJ
#mkdir libicu70
#ar p %{SOURCE3} data.tar.zst | tar -x --use-compress-program=unzstd -C libicu70 --strip-components=4
#mv libicu70/libicuuc.so.70.1                                          .%{app_libs_dir}/dcv/libicuuc.so.70
#mv libicu70/libicudata.so.70.1                                        .%{app_libs_dir}/dcv/libicudata.so.70

patchelf --set-rpath '$ORIGIN' --force-rpath                          .%{app_libs_dir}/dcv/dcvclientbin
patchelf --set-rpath '$ORIGIN' --force-rpath                          .%{app_libs_dir}/dcv/libdcv.so
#patchelf --set-rpath '$ORIGIN' --force-rpath                          .%{app_libs_dir}/dcv/libharfbuzz-icu.so.0
#patchelf --set-rpath '$ORIGIN' --force-rpath                          .%{app_libs_dir}/dcv/libicuuc.so.70
#patchelf --replace-needed libjbig.so.0       libjbig.so.2.1           .%{app_libs_dir}/dcv/libtiff.so.6
#patchelf --replace-needed libicuuc.so.70     libicuuc.so.71           .%{app_libs_dir}/dcv/libharfbuzz-icu.so.0

# Caches
#cd .%{app_libs_dir}/dcv/
#./gdk-pixbuf-query-loaders gdk-pixbuf-2.0/2.10.0/loaders/*.so | sed "s#%{_builddir}/%{name}-%{version}##" > gdk-pixbuf-2.0/2.10.0/loaders.cache
#./gtk-query-immodules-3.0  gtk-3.0/3.0.0/immodules/*.so       | sed "s#%{_builddir}/%{name}-%{version}##" > gtk-3.0/3.0.0/immodules.cache
rm -rf .%{app_libs_dir}/dcv/{gdk-pixbuf-query-loaders,gtk-query-immodules-3.0}
rm -rf .%{app_libs_dir}/dcv/{gdk-pixbuf-2.0,gtk-3.0,gstreamer-1.0,gio,sasl2}
rm -rf .%{app_libs_dir}/dcv/{libgdk_pixbuf-2.0.so.0,libgtk-3.so.0,libgdk-3.so.0}
rm -rf \
       .%{app_libs_dir}/dcv/libatk-1.0.so.0 \
       .%{app_libs_dir}/dcv/libavcodec.so.60 \
       .%{app_libs_dir}/dcv/libavutil.so.58 \
       .%{app_libs_dir}/dcv/libcairo-gobject.so.2 \
       .%{app_libs_dir}/dcv/libcairo-script-interpreter.so.2 \
       .%{app_libs_dir}/dcv/libcairo.so.2 \
       .%{app_libs_dir}/dcv/libepoxy.so.0 \
       .%{app_libs_dir}/dcv/libexpat.so.1 \
       .%{app_libs_dir}/dcv/libffi.so.8 \
       .%{app_libs_dir}/dcv/libfontconfig.so.1 \
       .%{app_libs_dir}/dcv/libfreetype.so.6 \
       .%{app_libs_dir}/dcv/libfribidi.so.0 \
       .%{app_libs_dir}/dcv/libgailutil-3.so.0 \
       .%{app_libs_dir}/dcv/libgio-2.0.so.0 \
       .%{app_libs_dir}/dcv/libglib-2.0.so.0 \
       .%{app_libs_dir}/dcv/libgmodule-2.0.so.0 \
       .%{app_libs_dir}/dcv/libgobject-2.0.so.0 \
       .%{app_libs_dir}/dcv/libgraphene-1.0.so.0 \
       .%{app_libs_dir}/dcv/libgstallocators-1.0.so.0 \
       .%{app_libs_dir}/dcv/libgstapp-1.0.so.0 \
       .%{app_libs_dir}/dcv/libgstaudio-1.0.so.0 \
       .%{app_libs_dir}/dcv/libgstbase-1.0.so.0 \
       .%{app_libs_dir}/dcv/libgstreamer-1.0.so.0 \
       .%{app_libs_dir}/dcv/libgstvideo-1.0.so.0 \
       .%{app_libs_dir}/dcv/libgthread-2.0.so.0 \
       .%{app_libs_dir}/dcv/libharfbuzz-icu.so.0 \
       .%{app_libs_dir}/dcv/libharfbuzz.so.0 \
       .%{app_libs_dir}/dcv/libharfbuzz-subset.so.0 \
       .%{app_libs_dir}/dcv/libjpeg.so.62 \
       .%{app_libs_dir}/dcv/libjson-glib-1.0.so.0 \
       .%{app_libs_dir}/dcv/liblmdb.so \
       .%{app_libs_dir}/dcv/liblz4.so.1 \
       .%{app_libs_dir}/dcv/libnghttp2.so.14 \
       .%{app_libs_dir}/dcv/libopus.so.0 \
       .%{app_libs_dir}/dcv/liborc-0.4.so.0 \
       .%{app_libs_dir}/dcv/libpango-1.0.so.0 \
       .%{app_libs_dir}/dcv/libpangocairo-1.0.so.0 \
       .%{app_libs_dir}/dcv/libpangoft2-1.0.so.0 \
       .%{app_libs_dir}/dcv/libpangoxft-1.0.so.0 \
       .%{app_libs_dir}/dcv/libpcre2-8.so.0 \
       .%{app_libs_dir}/dcv/libpixman-1.so.0 \
       .%{app_libs_dir}/dcv/libprotobuf-c.so.1 \
       .%{app_libs_dir}/dcv/libpsl.so.5 \
       .%{app_libs_dir}/dcv/librsvg-2.so.2 \
       .%{app_libs_dir}/dcv/libsasl2.so.3 \
       .%{app_libs_dir}/dcv/libsoup-3.0.so.0 \
       .%{app_libs_dir}/dcv/libtiff.so.6 \
       .%{app_libs_dir}/dcv/libturbojpeg.so.0 \
       .%{app_libs_dir}/dcv/libvpx.so.8 \
       .%{app_libs_dir}/dcv/libwayland-client.so.0 \
       .%{app_libs_dir}/dcv/libwayland-cursor.so.0 \
       .%{app_libs_dir}/dcv/libwayland-egl.so.1 \
       .%{app_libs_dir}/dcv/libz.so.1

rm -rf .%{app_libs_dir}/dcv/gst-plugin-scanner

%install
mv usr %{buildroot}/

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

%{app_libs_dir}/dcv/libdcv.so
%{app_libs_dir}/dcv/libdcvwebauthnredirection.so

%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/com.amazon.workspacesclient.dcv.gschema.xml
%{_datadir}/glib-2.0/schemas/com.amazon.workspacesclient.gschema.xml
%{_datadir}/icons/hicolor/*
%{_datadir}/locale/*

%license %{_datadir}/doc/%{app_name}/copyright

%changelog
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
