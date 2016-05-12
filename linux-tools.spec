Name:           linux-tools
Version:        4.5.4
Release:        208
License:        GPL-2.0
Summary:        The Linux kernel tools (perf)
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.5.4.tar.xz

%define kversion %{version}-%{release}.native

BuildRequires:  bash >= 2.03
BuildRequires:  bc
# For bfd support in perf/trace
BuildRequires:  binutils-dev
BuildRequires:  elfutils
BuildRequires:  elfutils-dev
BuildRequires:  kmod
BuildRequires:  make >= 3.78
BuildRequires:  openssl
BuildRequires:  openssl-dev
BuildRequires:  flex bison
BuildRequires:  ncurses-dev
BuildRequires:  binutils-dev
BuildRequires:  slang-dev
BuildRequires:  libunwind-dev
BuildRequires:  python-dev
BuildRequires:  zlib-dev
BuildRequires:  xz-dev
BuildRequires:  numactl-dev
BuildRequires:  perl

# don't srip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

# Serie    00XX: mainline, CVE, bugfixes patches
# GCC 6 fix
Patch0001: 0001-perf-pmu-Fix-misleadingly-indented-assignment-whites.patch
Patch0002: 0002-perf-tools-Fix-unused-variables-x86_-32-64-_regoffse.patch


%description
The Linux kernel tools perf/trace.

%prep
%setup -q -n linux-4.5.4

# Serie    00XX: mainline, CVE, bugfixes patches
# GCC 6 fix
%patch0001 -p1
%patch0002 -p1

# Serie    01XX: Clear Linux patches

# Serie    XYYY: Extra features modules

%build

BuildTools() {
    pushd tools/perf
    sed -i '/# Define NO_GTK2/a NO_GTK2 = 1' Makefile.perf
    # TODO: Fix me
    # error message: ld: XXX.o: plugin needed to handle lto object
    sed -i '/# Define NO_LIBPYTHON/a NO_LIBPYTHON = 1' Makefile.perf
    make -s %{?sparse_mflags}
    popd
    pushd tools/power/x86/turbostat
    make
    popd
}

BuildTools

%install

InstallTools() {
    pushd tools/perf
    %make_install prefix=/usr
    popd
    pushd tools/power/x86/turbostat
    %make_install prefix=/usr
    popd
}

InstallTools

# Move bash-completion
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mv %{buildroot}%{_sysconfdir}/bash_completion.d/perf %{buildroot}%{_datadir}/bash-completion/completions/perf
rmdir %{buildroot}%{_sysconfdir}/bash_completion.d
rmdir %{buildroot}%{_sysconfdir}



%files
%{_bindir}/trace
%{_bindir}/perf
/usr/libexec/perf-core
/usr/lib64/traceevent/plugins/
%{_datadir}/bash-completion/completions/*
/usr/bin/turbostat
/usr/share/man/man8/turbostat.8
/usr/share/doc/perf-tip/tips.txt
