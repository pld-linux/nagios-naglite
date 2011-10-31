%define		pname	naglite
%define		php_min_version 5.1.1
%include	/usr/lib/rpm/macros.php
Summary:	Naglite3 – Nagios status monitor for a NOC or operations room
Name:		nagios-%{pname}
Version:	1.5
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	https://github.com/saz/Naglite3/tarball/master/%{pname}.tgz
# Source0-md5:	29d7f404e6f51a0e0758478ef30a5611
Source1:	apache.conf
Source2:	lighttpd.conf
Patch0:		paths.patch
URL:		https://github.com/saz/Naglite3
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-date
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{pname}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Full screen Nagios status monitor. Fits nicely in your NOC or
operations room. Inspired by Naglite and Naglite2.

%prep
%setup -qc
mv *-Naglite3-*/* .
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}
cp -p *.php *.css $RPM_BUILD_ROOT%{_appdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base >= 1.3.37-3
%webapp_register apache %{_webapp}

%triggerin -- apache1 < 1.3.37-3, apache1-base >= 1.3.37-3
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
