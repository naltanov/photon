Summary:          NFS client utils
Name:             nfs-utils
Version:          2.3.3
Release:          8%{?dist}
License:          GPLv2+
URL:              http://sourceforge.net/projects/nfs
Group:            Applications/Nfs-utils-client
Source0:          http://downloads.sourceforge.net/nfs/%{name}-%{version}.tar.xz
%define sha512    nfs-utils=5025ccd7699ac1a0fdbd8b18ed8b33ea89230158320d809ec51e73f831100db75dceaddde481d911eeca9059caa521d155c2d14d014d75f091f432aad92a9716
Source1:          nfs-utils.defaults
Patch0:           0001-service-file-nfs-utils-conf.patch
Vendor:           VMware, Inc.
Distribution:     Photon
BuildRequires:    libtool
BuildRequires:    krb5-devel
BuildRequires:    libcap-devel
BuildRequires:    libtirpc-devel
BuildRequires:    python3-devel
BuildRequires:    libevent-devel
BuildRequires:    device-mapper-devel
BuildRequires:    systemd-devel
BuildRequires:    keyutils-devel
BuildRequires:    sqlite-devel
BuildRequires:    libgssglue-devel
BuildRequires:    e2fsprogs-devel
Requires:         libtirpc
Requires:         rpcbind
Requires:         shadow
Requires:         python3-libs
Requires:         libnfsidmap
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

%package -n libnfsidmap
Summary: NFSv4 User and Group ID Mapping Library
Provides:  libnfsidmap
License:   BSD
Conflicts: %{name} < 2.3.3-8

%description -n libnfsidmap
Library that handles mapping between names and ids for NFSv4.

%package -n libnfsidmap-devel
Summary:   Development files for the libnfsidmap library
Requires:  libnfsidmap
Conflicts: %{name} < 2.3.3-8

%description -n libnfsidmap-devel
This package includes header files and libraries necessary for
developing programs which use the libnfsidmap library.

%description
The nfs-utils package contains simple nfs client service.

%prep
%autosetup -n %{name}-%{version} -p1
#not prevent statd to start
sed -i "/daemon_init/s:\!::" utils/statd/statd.c
sed '/unistd.h/a#include <stdint.h>' -i support/nsm/rpc.c
find . -iname "*.py" | xargs -I file sed -i '1s/python/python3/g' file
# fix --with-rpcgen=internal
sed -i 's/RPCGEN_PATH" =/rpcgen_path" =/' configure

%build
%configure --enable-libmount-mount     \
           --without-tcp-wrappers      \
           --enable-gss                \
           --enable-svcgss             \
           --enable-nfsv4              \
           --with-rpcgen=internal      \
           --disable-static
# fix building against new gcc
sed -i -E 's/^(CFLAGS = .*)$/\1 -Wno-error=strict-prototypes/' support/nsm/Makefile
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -v -m644 utils/mount/nfsmount.conf %{_sysconfdir}/nfsmount.conf
mkdir -p %{buildroot}/lib/systemd/system/
mkdir -p %{buildroot}%{_sysconfdir}/default
mkdir -p %{buildroot}%{_sysconfdir}/export.d
mkdir -p %{buildroot}/var/lib/nfs/v4recovery
touch %{buildroot}%{_sysconfdir}/exports
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/default/nfs-utils
install -m644 systemd/nfs-utils.service %{buildroot}%{_unitdir}
#For backward compatibility
ln -s   %{_prefix}%{_unitdir}/nfs-utils.service %{buildroot}%{_unitdir}/nfs-client.service
install -m644 systemd/nfs-client.target %{buildroot}%{_unitdir}
install -m644 systemd/rpc-statd.service %{buildroot}%{_unitdir}
install -m644 systemd/rpc-statd-notify.service %{buildroot}%{_unitdir}
install -m644 systemd/nfs-server.service %{buildroot}%{_unitdir}
install -m644 systemd/nfs-mountd.service %{buildroot}%{_unitdir}
install -m644 systemd/proc-fs-nfsd.mount %{buildroot}%{_unitdir}
install -m644 systemd/nfs-idmapd.service %{buildroot}%{_unitdir}
install -m644 systemd/rpc_pipefs.target  %{buildroot}%{_unitdir}
install -m644 systemd/var-lib-nfs-rpc_pipefs.mount  %{buildroot}%{_unitdir}
install -m644 systemd/rpc-svcgssd.service %{buildroot}%{_unitdir}
install -m644 systemd/rpc-gssd.service %{buildroot}%{_unitdir}
install -m644 systemd/nfs-blkmap.service %{buildroot}%{_unitdir}
install -m644 systemd/auth-rpcgss-module.service %{buildroot}%{_unitdir}
find %{buildroot}/%{_libdir} -name '*.la' -delete
install -vdm755 %{buildroot}/usr/lib/systemd/system-preset
echo "disable nfs-server.service" > %{buildroot}/usr/lib/systemd/system-preset/50-nfs-server.preset

%check
#ignore test that might require additional setup
sed -i '/check_root/i \
exit 77' tests/t0001-statd-basic-mon-unmon.sh
make %{?_smp_mflags} check

%pre
if ! getent group nobody >/dev/null; then
    groupadd -r nobody
fi
if ! getent passwd nobody >/dev/null; then
    useradd -g named -s /bin/false -M -r nobody
fi

%post
/sbin/ldconfig
%systemd_post nfs-server.service

%preun
%systemd_preun nfs-server.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart nfs-server.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/default/nfs-utils
%config(noreplace) %{_sysconfdir}/exports
/sbin/*
%{_mandir}/*
%{_sbindir}/*
%{_sharedstatedir}/*
%{_unitdir}/*.service
%{_libdir}/systemd/system-preset/50-nfs-server.preset
/lib/systemd/system/*

%files -n libnfsidmap
%defattr(-,root,root)
%{_libdir}/libnfsidmap.so.*
%{_libdir}/libnfsidmap/*.so
%{_mandir}/man3/nfs4_uid_to_name.*
%{_mandir}/man8/nfsidmap.*
%{_mandir}/man8/idmapd.8.gz

%files -n libnfsidmap-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/libnfsidmap.pc
%{_includedir}/nfsidmap.h
%{_includedir}/nfsidmap_plugin.h
%{_libdir}/libnfsidmap.so

%changelog
* Thu Jun 15 2023 Piyush Gupta <gpiyush@vmware.com> 2.3.3-8
- Add devel sub pkg.
* Mon May 29 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.3.3-7
- Include rpc-gssd.service file
* Wed Apr 12 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.3.3-6
- Bump version as a part of libevent upgrade
* Fri Mar 18 2022 Harinadh D <hdommaraju@vmware.com> 2.3.3-5
- enable svcgss
* Tue Nov 17 2020 Tapas Kundu <tkundu@vmware.com> 2.3.3-4
- Restrict nfs-mountd to start after rpcbind.socket
* Wed Oct 28 2020 Dweep Advani <dadvani@vmware.com> 2.3.3-3
- Removed redundant dependency on libnfsidmap
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 2.3.3-2
- Fix compilation issue against glibc-2.28
- Use internal rpcgen, disable librpcsecgss dependency.
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.3.3-1
- Update to 2.3.3
* Thu Jun 07 2018 Anish Swaminathan <anishs@vmware.com> 2.3.1-2
- Add noreplace qualifier to config files
* Fri Jan 26 2018 Xiaolin Li <xiaolinl@vmware.com> 2.3.1-1
- Update to 2.3.1 and enable nfsv4
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.1-7
- No direct toybox dependency, shadow depends on toybox
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.1-6
- Requires shadow or toybox
* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.1-5
- Fix compilation issue for glibc-2.26
* Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.1-4
- Add check and ignore test that fails.
* Tue Aug 8 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.1-3
- Alter nfs-server and nfs-mountd service files to use
- environment file and port opts.
* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.1-2
- Build with python3.
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.1-1
- Update to 2.1.1
* Fri Dec 16 2016 Nick Shi <nshi@vmware.com> 1.3.3-6
- Requires rpcbind.socket upon starting rpc-statd service (bug 1668405)
* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.3-5
- add shadow to requires
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.3.3-4
- Removed packaging of debug files
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.3-3
- GA - Bump release of all rpms
* Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.3-2
- Add nfs-server.service to rpm.
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.3-1
- Updated to version 1.3.3
* Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.2-2
- Adding systemd service files
* Tue Jul 14 2015 Rongrong Qiu <rqiu@vmware.com> 1.3.2-1
- Initial build.  First version
