Summary:        Mobile broadband modem manager
Name:           ModemManager
Version:        1.14.2
Release:        5%{?dist}
URL:            https://www.freedesktop.org
License:        GPLv2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.freedesktop.org/software/ModemManager/ModemManager-%{version}.tar.xz
%define sha512  %{name}=850217895df92e4037e94afd0947de8079d2b49b085d96af7cdb5714ed87d40e9a892750c8392370c940a259b00bfccad67fa09a2a8861ce1e6d50aa355f7bc9

BuildRequires:  libqmi-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libgudev-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-libs
BuildRequires:  gcc
BuildRequires:  pkg-config
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  libxslt

%if 0%{?with_check}
BuildRequires:  dbus-devel
%endif

Requires:       libgudev
Requires:       libqmi
Requires:       gobject-introspection
%description
ModemManager provides a unified high level API for communicating
with mobile broadband modems, regardless of the protocol used to
communicate with the actual device.

%package      devel
Summary:      Header and development files for ModemManager
Requires:     %{name} = %{version}-%{release}
Requires:     libqmi-devel
Requires:     gobject-introspection-devel
%description  devel
It contains the libraries and header files for ModemManager

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --enable-more-warnings=no \
    --without-qmi \
    --without-mbim

%make_build

%install
%make_install UDEV_BASE_DIR=%{_libdir}/udev %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_datadir}/ModemManager/*.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_bindir}/mmcli
%{_sbindir}/ModemManager
%{_libdir}/libmm-glib.so*
%{_libdir}/girepository-1.0/ModemManager-1.0.typelib
%{_libdir}/ModemManager/*
%{_libdir}/systemd/system/ModemManager.service
%exclude %dir %{_libdir}/debug
%{_mandir}/man1/mmcli.1.gz
%{_mandir}/man8/ModemManager.8.gz
%{_datadir}/dbus-1/*
%{_datadir}/locale/*
%{_datadir}/bash-completion/*
%{_datadir}/gir-1.0/ModemManager-1.0.gir
%exclude %{_datadir}/icons
%{_udevrulesdir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/ModemManager/*
%{_includedir}/libmm-glib/*
%{_libdir}/pkgconfig/ModemManager.pc
%{_libdir}/pkgconfig/mm-glib.pc

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-5
- Remove .la files
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-4
- Exclude debug symbols properly
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.14.2-3
- Add build requires
* Wed Nov 18 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.2-2
- Fix make check
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.2-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-1
- Initial build. First version
