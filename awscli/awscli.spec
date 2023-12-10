%define debug_package %{nil}
%define _build_id_links none

%global srcname aws-cli
%global __provides_exclude_from %{_libexecdir}/%{srcname}
%global __requires_exclude_from %{_libexecdir}/%{srcname}

Name:           awscli
# here you can find a new tag
# https://github.com/aws/aws-cli/tree/v2
# https://github.com/aws/aws-cli/tags
Version:        2.15.0
Release:        1%{?dist}
Summary:        Universal Command Line Interface for Amazon Web Services

License:        ASL 2.0 and MIT
URL:            https://aws.amazon.com/cli
Source0:        https://github.com/aws/%{srcname}/archive/refs/tags/%{version}.tar.gz

BuildRequires: make
BuildRequires: upx
%if 0%{?el8}
BuildRequires: python38
%elif 0%{?fc39}%{?fc40}
%global python3 /usr/bin/python3.11
BuildRequires:  python3.11-devel
%else
BuildRequires: python > 3.8
%endif

%description
The AWS Command Line Interface (AWS CLI) is a unified tool to manage your AWS services.
The AWS CLI v2 offers several new features including improved installers,
new configuration options such as AWS Single Sign-On (SSO), and various interactive features.
AWS CLI v2 builds on AWS CLI v1 and includes a number of features and enhancements based on community feedback.
https://aws.amazon.com/blogs/developer/aws-cli-v2-is-now-generally-available/

%prep
%setup -q -n %{srcname}-%{version}

%build
export PIP_DISABLE_PIP_VERSION_CHECK=1
%set_build_flags
export PYTHON=%{python3}
%_configure --with-download-deps --with-install-type=portable-exe --prefix=%_prefix --libdir=%{_libexecdir}
%make_build

%install
%make_install
rm -rf %{buildroot}%{_libexecdir}/%{srcname}/%{name}/examples \
       %{buildroot}%{_libexecdir}/%{srcname}/docutils
find   %{buildroot}%{_libexecdir} -type f -name "*.rst" -delete

ln -sf ../libexec/%{srcname}/aws           %{buildroot}%{_bindir}/aws
ln -sf ../libexec/%{srcname}/aws_completer %{buildroot}%{_bindir}/aws_completer

%files
%doc README.rst
%license LICENSE.txt
%{_bindir}/aws
%{_bindir}/aws_completer
%{_libexecdir}/%{srcname}

%check
%{buildroot}%{_bindir}/aws --version

%changelog
* Sun Dec 10 2023 Anatolii Vorona - 2.15.0-1
- bump version

* Tue Apr 25 2023 Anatolii Vorona - 2.11.15-1
- bump version; first testing c8/c9 stream and al2023

* Thu Mar 23 2023 Anatolii Vorona - 2.11.5-1
- init spec aws-cli v2
