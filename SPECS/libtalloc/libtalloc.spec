Summary:    Talloc is a hierarchical, reference counted memory pool system
Name:       libtalloc
Version:    2.1.14
Release:    3%{?dist}
License:    LGPLv3+
URL:        https://talloc.samba.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%define sha512  talloc=1fcc70bf283a4d9fb61faf1c57f80a9c158efbe996452740db9755e879ad72ee7bff6f6c9bed358e085c5c7f97c78800bb903161143af2202952b702141cc130
BuildRequires: libxslt
BuildRequires: docbook-xsl
BuildRequires: python2-devel

%description
Libtalloc alloc is a hierarchical, reference counted memory pool system with destructors. It is the core memory allocator used in Samba.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libtalloc-devel package contains libraries and header files for libtalloc

%package -n python-talloc
Group: Development/Libraries
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description -n python-talloc
Python 2 libraries for creating bindings using talloc

%package -n python-talloc-devel
Group: Development/Libraries
Summary: Development libraries for python-talloc
Requires: python-talloc = %{version}-%{release}

%description -n python-talloc-devel
Development libraries for python-talloc

%prep
%autosetup -p1 -n talloc-%{version}

%build
%configure --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules
make %{?_smp_mflags} V=1

%install
%make_install
rm -f %{buildroot}/usr/share/swig/*/talloc.i

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libtalloc.so.*

%files devel
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz

%files -n python-talloc
%{_libdir}/libpytalloc-util.so.*
%{_libdir}/python2.7/site-packages/*

%files -n python-talloc-devel
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.so

%changelog
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.1.14-3
-   Bump version as a part of libxslt upgrade
*   Mon Jan 06 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.1.14-2
-   Added python2-devel as a build requirement
*   Tue Sep 11 2018 Bo Gan <ganb@vmware.com> 2.1.14-1
-   Update to 2.1.14
*   Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.1.9-2
-   Copy libraries and add a patch for path regarding %check
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 2.1.9-1
-   Initial packaging
