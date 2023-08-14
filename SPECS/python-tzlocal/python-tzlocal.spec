%define srcname tzlocal

Summary:        tzinfo object for the local timezone.
Name:           python3-tzlocal
Version:        4.2
Release:        1%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/regebro/tzlocal

Source0: https://files.pythonhosted.org/packages/source/t/tzlocal/tzlocal-%{version}.tar.gz
%define sha512 %{srcname}=5d1000bd8756ca2678655dbeedcfd6ef8d709503293303c98a48af234aca0d1525913585d679759c6fd7d4c5ef046c98384ee6e7a9eba769f81d05173ff0d77f

BuildRequires: python3-devel
BuildRequires: python3-six
BuildRequires: python3-setuptools
BuildRequires: python3-xml

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-pip
BuildRequires: python3-hypothesis
BuildRequires: python3-pytz-deprecation-shim
BuildRequires: tzdata
%endif

Requires: python3
Requires: python3-pytz
Requires: python3-pytz-deprecation-shim

BuildArch: noarch

%description
This Python module returns a tzinfo object with the local timezone information under Unix and Win-32.
It requires pytz, and returns pytz tzinfo objects. This module attempts to fix a glaring hole in pytz,
that there is no way to get the local timezone information, unless you know the zoneinfo name,
and under several Linux distros that’s hard or impossible to figure out.
Also, with Windows different timezone system using pytz isn’t of much use,
unless you separately configure the zoneinfo timezone name.
With tzlocal you only need to call get_localzone(),
and you will get a tzinfo object with the local time zone info.
On some Unices you will still not get to know what the timezone name is,
but you don’t need that when you have the tzinfo file.
However, if the timezone name is readily available it will be used.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
pip3 install tomli mocker pytest-mock
%pytest -k 'not symlink_localtime and not conflicting and not noconflict'

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat Aug 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.2-1
- Upgrade to v4.2
- Add python3-pytz-deprecation-shim to requires
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.1-2
- Bump up to compile with python 3.10
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 1.5.1-3
- Mass removal python2
* Mon Nov 26 2018 Tapas Kundu <tkundu@vmware.com> 1.5.1-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.5.1-1
- Update to version 1.5.1
* Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4-1
- Initial packaging for Photon
