# apxs script location
%{!?_httpd_apxs: %global _httpd_apxs %{_bindir}/apxs}
%{!?_httpd_moddir: %global _httpd_moddir %{_libdir}/httpd/modules}
%{!?_httpd_confdir: %global _httpd_confdir %{_sysconfdir}/httpd/conf.d}

# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}

%global httpd24 1
%global rundir /run

Name:   mod_cgroup
Version:  2.0
Release:  0%{?dist}
Summary:  Control group support for Apache 2
Group:    System Environment/Daemons
License:  LGPL 3.0
URL:    https://github.com/apisnetworks/mod_cgroup
Source0:  https://github.com/apisnetworks/mod_cgroup/archive/%{name}-%{version}.tar.gz
Source1:  mod_cgroup.conf
Source2:  mod_cgroup.te
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:  httpd-devel >= 2.4, pkgconfig, fail2ban
Requires: httpd-mmn = %{_httpd_mmn}

%description
mod_cgroup provides a system administrator with the capability to provide 
predictable service levels for each virtual host declared in httpd.

%prep
%setup -q -n %{name}-%{version}
cp -p %{SOURCE1} cgroup.conf
cp -p %{SOURCE2} cgroup.te

%build
%{_httpd_apxs} -c -Wc,"%{optflags} -Wall -pedantic -std=c99" -lcgroup mod_cgroup.c


%install
install -Dm 755 .libs/mod_cgroup.so $RPM_BUILD_ROOT%{_httpd_moddir}/mod_cgroup.so
install -Dp -m 0644 cgroup.conf %{buildroot}%{_httpd_confdir}/cgroup.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md LICENSE cgroup.te
%config(noreplace) %{_httpd_confdir}/cgroup.conf
%{_httpd_moddir}/*.so

%changelog
* Sat May 05 2018 Matt Saladna <matt@apisnetworks.com> - 2.0-0
- Initial release
