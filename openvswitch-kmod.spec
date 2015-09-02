# snapshot is the date YYYYMMDD of the snapshot
# snap_git is the 8 git sha digits of the last commit
# Use ovs-snapshot.sh to create the tarball.
#% define snapshot .git20150730
#% define snap_gitsha -git72bfa562

%global kmodinstdir_prefix  /lib/modules/
%global kmodname openvswitch
%global kmodinstdir_postfix /updates/%{kmodname}

Name: openvswitch-kmod
Version: 2.4.0
Release: 1%{?snapshot}%{?dist}

Summary: Open vSwitch Kernel Modules
Group: System Environment/Kernel
# The entire source code is ASL 2.0 except datapath/ which is GPLv2
License: GPLv2
URL: http://www.openvswitch.org/
Source0: http://openvswitch.org/releases/openvswitch-%{version}%{?snap_gitsha}.tar.gz
Source11: openvswitch-kmod-kernel-version

Patch0: no_depmod.patch
Patch1: ipv6_checksum.patch

%global kernel_version %{expand:%(cat %{SOURCE11} 2>/dev/null)}

%description
The openvswitch out of tree kernel module


%package      -n kmod-openvswitch
Summary:         Metapackage which tracks in openvswitch kernel module for newest kernel
Group:           System Environment/Kernel

Provides:        openvswitch-kmod = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:        kmod-openvswitch-%{kernel_version}.%{_arch} >= %{?epoch:%{epoch}:}%{version}-%{release}

%description  -n kmod-openvswitch
This is a meta-package without payload which sole purpose is to require the
openvswitch kernel module(s) for the newest kernel.
to make sure you get it together with a new kernel.

%files        -n kmod-openvswitch
%defattr(644,root,root,755)


%package       -n kmod-openvswitch-%{kernel_version}.%{_arch}
Summary:          openvswitch kernel module(s) for %{kernel_version}.%{_arch}
Group:            System Environment/Kernel
Provides:         kernel-modules-for-kernel = %{kernel_version}.%{_arch}
Provides:         openvswitch-kmod = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post):   /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod
Requires:         kernel-uname-r = %{kernel_version}.%{_arch}
BuildRequires:    kernel-devel-uname-r = %{kernel_version}.%{_arch}

%post          -n kmod-openvswitch-%{kernel_version}.%{_arch}
/usr/sbin/depmod -aeF /boot/System.map-%{kernel_version}.%{_arch} %{kernel_version}.%{_arch} > /dev/null || :
%postun        -n kmod-openvswitch-%{kernel_version}.%{_arch}
/usr/sbin/depmod  -aF /boot/System.map-%{kernel_version}.%{_arch} %{kernel_version}.%{_arch} &> /dev/null || :

%description  -n kmod-openvswitch-%{kernel_version}.%{_arch}
This package provides the openvswitch kernel modules built for the Linux
kernel %{kernel_version}.%{_arch} for the %{_target_cpu} family of processors.

%prep
%setup -q -T -b 0 -n %{kmodname}-%{version}%{?snap_gitsha}
%patch0 -p1
%patch1 -p1

%build
%if 0%{?snap_gitsha:1}
# fix the snapshot unreleased version to be the released one.
sed -i.old -e "s/^AC_INIT(openvswitch,.*,/AC_INIT(openvswitch, %{version},/" configure.ac
./boot.sh
%endif

%configure --disable-ssl --with-linux=%{_usrsrc}/kernels/%{kernel_version}.%{_arch}
%ifarch ppc64le
export LDFLAGS=''
%endif
make %{?_smp_mflags} -C datapath/linux

%install
rm -rf %{buildroot}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=%{kmodinstdir_postfix}
make -C datapath/linux modules_install
rm -f %{buildroot}/%{kmodinstdir_prefix}/%{kernel_version}.%{_arch}/modules.* 

%clean
rm -rf %{buildroot}

%files         -n kmod-openvswitch-%{kernel_version}.%{_arch}
%defattr(644,root,root,755)
%dir %{kmodinstdir_prefix}/%{kernel_version}.%{_arch}/updates
%{kmodinstdir_prefix}/%{kernel_version}.%{_arch}/%{kmodinstdir_postfix}


%changelog
* Wed Sep 02 2015 Jason Kölker <jason@koelker.net>
- Initial SPEC

