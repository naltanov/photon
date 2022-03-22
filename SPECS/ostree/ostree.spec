Summary:        Git for operating system binaries
Name:           ostree
Version:        2017.4
Release:        5%{?dist}
License:        LGPLv2+
URL:            http://live.gnome.org/OSTree
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnome.org/pub/GNOME/sources/ostree/%{version}/%{name}-%{version}.tar.gz
%define sha1    %{name}=eb3546c552849ace2f4e3701bc0b826611f569cc
Source1:        bsdiff-1edf9f6.tar.bz2
%define sha1    bsdiff-1edf9f6=cedfbec437a1cd084b4f26cbfc79973966e07bb0
Source2:        libglnx-602fdd9.tar.bz2
%define sha1    libglnx-602fdd9=76821ae2a2619ad965bb23d8e7f5883da4855dee
Source3:        91-ostree.preset

Patch0:         libglnx-basename-implementation.patch

BuildRequires:  which
BuildRequires:  libgsystem-devel
BuildRequires:  xz-devel
BuildRequires:  gtk-doc
BuildRequires:  e2fsprogs-devel
BuildRequires:  libsoup-devel
BuildRequires:  autogen
BuildRequires:  attr-devel
BuildRequires:  fuse-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  python2-libs
BuildRequires:  python2
BuildRequires:  gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  gobject-introspection-python
BuildRequires:  gpgme-devel
BuildRequires:  libcap-devel
BuildRequires:  libsoup
BuildRequires:  libsoup-devel
BuildRequires:  mkinitcpio
BuildRequires:  dracut
BuildRequires:  dracut-tools
BuildRequires:  systemd-devel
BuildRequires:  libarchive
BuildRequires:  libarchive-devel

Requires:       fuse
Requires:       libgsystem
Requires:       gpgme
Requires:       libassuan
Requires:       libgpg-error
Requires:       systemd
Requires:       libsoup
Requires:       mkinitcpio
Requires:       dracut
Requires:       dracut-tools
Requires:       libarchive
Requires:       libgsystem

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%package devel
Summary: Development headers for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package includes the header files for the %{name} library

%prep
# Using autosetup is not feasible
%setup -q
tar xf %{SOURCE1} --no-same-owner --strip-components=1 -C bsdiff
tar xf %{SOURCE2} --no-same-owner --strip-components=1 -C libglnx
%patch0 -p1

%build
env NOCONFIGURE=1 ./autogen.sh
%configure \
    --disable-silent-rules \
    --enable-gtk-doc \
    --with-dracut \
    --with-mkinitcpio \
    --enable-libsoup-client-cert

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c" %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
install -D -m 0644 %{SOURCE3} %{buildroot}%{_presetdir}/91-ostree.preset
install -vdm 755 %{buildroot}/etc/ostree/remotes.d

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%postun
%systemd_postun_with_restart ostree-remount.service

%files
%doc COPYING README.md
%{_bindir}/ostree
%{_bindir}/rofiles-fuse
%{_libdir}/*.so.1*
%{_mandir}/man*/*.gz
%{_presetdir}/91-ostree.preset
%{_unitdir}/ostree*.service
%dir %{_prefix}/lib/dracut/modules.d/*ostree
%{_prefix}/lib/dracut/modules.d/98ostree/*
%{_sysconfdir}/grub.d/*ostree
%{_sysconfdir}/dracut.conf.d/ostree.conf
%{_sysconfdir}/ostree-mkinitcpio.conf
%dir %{_sysconfdir}/ostree/remotes.d
%{_libdir}/girepository-*/OSTree-*.typelib
%{_libexecdir}/libostree/grub2*
%{_libdir}/initcpio/*
%{_libdir}/ostree/ostree-prepare-root
%{_libdir}/ostree/ostree-remount
%exclude %{_libexecdir}/libostree/ostree-trivial-httpd

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%dir %{_datadir}/gtk-doc/html/ostree
%{_datadir}/gtk-doc/html/ostree/*
%{_datadir}/ostree/*
%{_datadir}/gir-1.0/OSTree-1.0.gir

%changelog
* Wed Aug 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 2017.4-5
- Bump up to use new icu lib.
* Wed Jul 17 2019 Ankit Jain <ankitja@vmware.com> 2017.4-4
- Added a patch to implement its own glnx-basename()
* Thu Aug 23 2018 Tapas Kundu <tkundu@vmware.com> 2017.4-3
- Corrected the git clone path for libglnx.
* Mon May 08 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2017.4-2
- Use libgsystem-devel to build instead of libgsystem.
* Mon Apr 17 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2017.4-1
- Update to 2017.4
* Wed Feb 01 2017 Xiaolin Li <xiaolinl@vmware.com> 2015.7-10
- libglnx: checkout commit 900b25f.
- bsdiff:  checkout commit 1edf9f6.
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.7-9
- BuildRequired attr-devel and libgpg-error-devel
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2015.7-8
- Change systemd dependency
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.7-7
- Use %setup instead of %autosetup
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 2015.7-6
- Modified %check
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2015.7-5
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2015.7-4
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 2015.7-3
- Remove commented steps.
* Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 2015.7-2
- Add dracut, mkinitcpio and libsoup as dependencies
* Wed Jun 17 2015 Anish Swaminathan <anishs@vmware.com> 2015.7-1
- Updated the version
* Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 2014.11-1
- Initial build. First version
