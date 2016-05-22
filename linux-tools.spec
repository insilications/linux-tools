Name:           linux-tools
Version:        4.6
Release:        210
License:        GPL-2.0
Summary:        The Linux kernel tools (perf)
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.6.tar.xz

BuildRequires:  bash
BuildRequires:  bc
BuildRequires:  binutils-dev
BuildRequires:  elfutils
BuildRequires:  elfutils-dev
BuildRequires:  kmod
BuildRequires:  make
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
BuildRequires:  xmlto
BuildRequires:  asciidoc
BuildRequires:  util-linux
BuildRequires:  libxml2-dev
BuildRequires:  libxslt
BuildRequires:  docbook-xml


%description
The Linux kernel tools perf/trace.

%prep
%setup -q -n linux-4.6

%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm

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
	pushd Documentation
	make man
	make DESTDIR=%{buildroot} install
	popd
    popd
    pushd tools/power/x86/turbostat
    %make_install prefix=/usr
    popd
}

InstallTools

# Move bash-completion
mkdir -p %{buildroot}/usr/share/bash-completion/completions
mv %{buildroot}/etc/bash_completion.d/perf %{buildroot}/usr/share/bash-completion/completions/perf
rmdir %{buildroot}/etc/bash_completion.d
rmdir %{buildroot}/etc

%files
/usr/bin/trace
/usr/bin/perf
/usr/libexec/perf-core
/usr/lib64/traceevent/plugins/
/usr/share/bash-completion/completions/*
/usr/bin/turbostat
/usr/share/man/man8/turbostat.8
/usr/share/man/man1
/usr/share/doc/perf-tip/tips.txt
