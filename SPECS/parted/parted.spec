Summary:        GNU Parted manipulates partition tables
Name:           parted
Version:        3.3
Release:        3%{?dist}
License:        GPLv3+
URL:            http://ftp.gnu.org/gnu/parted/parted-3.2.tar.xz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
%define sha512 parted=d1384694a491aa53bab6206fdeccd1d192de2ed379fe25aa865dd6aa06ed945a728e85b2ccc2fb23f5aa9dfee4a8bd8f0f2be1dd386cb8e8861b73382c6a07e4

Patch0:         parted-freelocale.patch

Conflicts:      toybox < 0.8.2-2

%description
This is useful for creating space for new operating systems,
reorganizing disk usage, copying data on hard disks and disk imaging.
The package contains a library, libparted, as well as well as a
command-line frontend, parted, which can also be used in scripts.

%prep
%autosetup -p1

%build
#Add a header to allow building with glibc-2.28 or later
sed -i '/utsname.h/a#include <sys/sysmacros.h>' libparted/arch/linux.c &&

%configure --without-readline --disable-debug \
	   --disable-nls --disable-device-mapper
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/*
%{_datadir}/*
%exclude %{_infodir}/dir

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-3
- Remove .la files
* Fri Jan 22 2021 Dweep Advani <dadvani@vmware.com> 3.3-2
- Remove conflict causing /usr/share/info/dir from packaging
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-8
- Do not conflict with toybox >= 0.8.2-2
* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 3.2-7
- Add conflict toybox.
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.2-6
- Fix compilation issue against glibc-2.28.
* Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-5
- Fix summary and description.
* Tue Jun 06 2017 ChangLee <changlee@vmware.com> 3.2-4
- Remove %check.
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.2-3
- Modified %check.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
- GA Bump release of all rpms.
* Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.2-1
- Initial version.
