Summary:	Power management service
Name:		upower
Version:	0.9.19
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://upower.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	f96955ff1a2e4f006937d6b5ea95afb8
URL:		http://upower.freedesktop.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libusbx-devel
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	udev-glib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pm-utils
Requires:	polkit
Requires:	udev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/upower

%description
upower provides a daemon, API and command line tools for
managing power devices attached to the system.

%package libs
Summary:	upower library
Group:		Development

%description libs
upower gobject library.

%package devel
Summary:	upower development files
Group:		Development
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib-devel

%description devel
upower development files.

%package apidocs
Summary:	upower API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
upower API documentation.

%prep
%setup -q

%{__sed} -i "s|bash|sh|" src/notify-upower.sh

%build
%{__autopoint}
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}	\
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	udevrulesdir=%{_prefix}/lib/udev/rules.d

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS HACKING NEWS README

%dir %{_libexecdir}
%attr(755,root,root) %{_bindir}/upower
%attr(755,root,root) %{_libexecdir}/upowerd

%dir %{_sysconfdir}/UPower
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/UPower/UPower.conf

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.UPower.conf
%config(noreplace) %verify(not md5 mtime size) %{_prefix}/lib/udev/rules.d/95-upower-battery-recall-*.rules
%config(noreplace) %verify(not md5 mtime size) %{_prefix}/lib/udev/rules.d/95-upower-csr.rules
%config(noreplace) %verify(not md5 mtime size) %{_prefix}/lib/udev/rules.d/95-upower-hid.rules
%config(noreplace) %verify(not md5 mtime size) %{_prefix}/lib/udev/rules.d/95-upower-wup.rules

%{_datadir}/dbus-1/system-services/org.freedesktop.UPower.service
%{_datadir}/polkit-1/actions/org.freedesktop.upower.policy
%{_datadir}/polkit-1/actions/org.freedesktop.upower.qos.policy
%{systemdunitdir}/upower.service
%dir %{_prefix}/lib/systemd/system-sleep
%attr(755,root,root) %{_prefix}/lib/systemd/system-sleep/notify-upower.sh

%{_mandir}/man1/upower.1*
%{_mandir}/man7/UPower.7*
%{_mandir}/man8/upowerd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/libupower-glib
%{_datadir}/gir-1.0/UPowerGlib-1.0.gir
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.Device.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.KbdBacklight.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.QoS.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.Wakeups.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.xml
%{_pkgconfigdir}/*.pc

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/UPower
%endif

