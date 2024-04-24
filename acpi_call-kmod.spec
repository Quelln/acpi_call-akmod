%global debug_package %{nil}
Name: acpi_call-kmod
Version: 1.2.2
Release: 1%{?dist}
Summary: Akmod package for acpi_call

License: GPL-3.0
URL: https://github.com/nix-community/acpi_call/
Source: https://github.com/nix-community/acpi_call/archive/ede6ea71353c39c6e111816bca3e7789a9a4eb5c.tar.gz
BuildRequires: kmodtool gcc make
Provides: acpi_call-kmod-common

ExclusiveArch: x86_64
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Akmod package for acpi_call

%prep
%{?kmodtool_check}

kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T
mkdir %{name}-%{version}-src
pushd %{name}-%{version}-src
tar xf %{SOURCE0}
popd


for kernel_version in %{?kernel_versions} ; do
 cp -a %{name}-%{version}-src _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/acpi_call-ede6ea71353c39c6e111816bca3e7789a9a4eb5c
 make -C ${kernel_version##*___} M=`pwd` modules
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/acpi_call-ede6ea71353c39c6e111816bca3e7789a9a4eb5c
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -m 0755 *.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 popd
done
chmod 0755 $RPM_BUILD_ROOT%{kmodinstdir_prefix}*%{kmodinstdir_postfix}/* || :
%{?akmod_install}
%clean
rm -rf $RPM_BUILD_ROOT

%package -n acpi_call-kmod-common
Summary: Dummy package
%description  -n acpi_call-kmod-common
dummy package
%files -n acpi_call-kmod-common



%package -n acpi_call-akmod-kmod-common
Summary: Dummy package
%description  -n acpi_call-akmod-kmod-common
dummy package
%files -n acpi_call-akmod-kmod-common
