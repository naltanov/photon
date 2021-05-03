Summary:        Tools and Utilities for interaction with SCSI devices.
Name:           sg3_utils
Version:        1.46
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/hreinecke/sg3_utils
Source0:        %{name}-%{version}.tar.gz
%define sha1    sg3_utils=0ba89a0b9140b469fde568a76361cfbc02e64338
Group:          System/Tools.
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       sg_utils.
BuildRequires:  lua-devel

%description
Linux tools and utilities to send commands to SCSI devices.

%package -n     libsg3_utils-devel
Summary:        Devel pacjage for sg3_utils.
Group:          Development/Library.

%description -n libsg3_utils-devel
Package containing static library object for development.

%prep
%setup -q

%build
#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' src/sg_dd.c src/sg_map26.c src/sg_xcopy.c

%configure

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -m 755 scripts/scsi_logging_level %{buildroot}/%{_bindir}
install -m 755 scripts/rescan-scsi-bus.sh %{buildroot}/%{_bindir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*
%{_libdir}/libsgutils2*.so.*

%files -n libsg3_utils-devel
%defattr(-,root,root)
%{_libdir}/libsgutils2.a
%{_libdir}/libsgutils2.la
%{_libdir}/libsgutils2.so
%{_includedir}/scsi/*

%changelog
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 1.46-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.44-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.43-2
-   Fix compilation issue against glibc-2.28
*   Tue Oct 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.43-1
-   Update to v1.43
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.42-2
-   GA - Bump release of all rpms
*   Thu Apr 14 2016 Kumar Kaushik <kaushikk@vmware.com> 1.42-1
-   Initial build. First version
