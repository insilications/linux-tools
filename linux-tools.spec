Name:           linux-tools
Version:        5.6
Release:        424
License:        GPL-2.0
Summary:        The Linux kernel tools (perf)
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.6.tar.xz

Requires: binutils

BuildRequires:  bash
BuildRequires:  bc
BuildRequires:  binutils-dev
BuildRequires:  binutils-staticdev
BuildRequires:  elfutils
BuildRequires:  elfutils-dev
BuildRequires:  kmod
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-dev
BuildRequires:  flex bison
BuildRequires:  ncurses-dev
BuildRequires:  slang-dev
BuildRequires:  libunwind-dev
BuildRequires:  libunwind-dev32
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
BuildRequires:  audit-dev
BuildRequires:  python3-dev python3-staticdev
BuildRequires:  python3
BuildRequires:  babeltrace-dev
BuildRequires:  zstd-dev
BuildRequires:  libcap-dev

Patch1: turbostat.patch
Patch2: vmlinux-location.patch
Patch3: 0001-Filter-out-link-time-optimization.patch
Patch4: 0001-Make-python-config-call-python3.8-compatable.patch

%description
The Linux kernel tools perf/trace.

%package hyperv
License:        GPL-2.0
Summary:        The Linux kernel hyperv daemon files
Group:          kernel

%description hyperv
Linux kernel hyperv daemon files

%prep
%setup -q -n linux-5.6
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export GCC_IGNORE_WERROR=1
export CFLAGS="-g1 -O3 -Wl,-z -Wl,now -Wl,-z -Wl,relro -Wl,-z,max-page-size=0x1000 -march=native -mtune=native -fgraphite-identity -O3 -Wall -Wl,--as-needed -Wl,--build-id=sha1 -Wl,--enable-new-dtags -Wl,--hash-style=gnu -Wl,-O2 -Wl,-z,now -Wl,-z,relro -falign-functions=32 -fasynchronous-unwind-tables -fdevirtualize-at-ltrans -floop-nest-optimize -fno-math-errno -fno-semantic-interposition -fno-stack-protector -fno-trapping-math -ftree-loop-distribute-patterns -ftree-loop-vectorize -ftree-vectorize -funroll-loops -fuse-ld=bfd -fuse-linker-plugin -malign-data=cacheline -fno-plt -mtls-dialect=gnu2 -Wl,-sort-common -pipe -I/usr/include/python3.8/ -fcommon"
export CXXFLAGS="-g1 -O3  -Wl,-z,max-page-size=0x1000 -march=native -mtune=native -fgraphite-identity -O3 -Wall -Wl,--as-needed -Wl,--build-id=sha1 -Wl,--enable-new-dtags -Wl,--hash-style=gnu -Wl,-O2 -Wl,-z,now -Wl,-z,relro -falign-functions=32 -fasynchronous-unwind-tables -fdevirtualize-at-ltrans -floop-nest-optimize -fno-math-errno -fno-semantic-interposition -fno-stack-protector -fno-trapping-math -ftree-loop-distribute-patterns -ftree-loop-vectorize -ftree-vectorize -funroll-loops -fuse-ld=bfd -fuse-linker-plugin -malign-data=cacheline -fno-plt -mtls-dialect=gnu2 -Wl,-sort-common -pipe -I/usr/include/python3.8/ -fcommon"
export LDFLAGS="-g1 -O3 -Wl,-z -Wl,now -Wl,-z -Wl,relro -Wl,-z,max-page-size=0x1000 -march=native -mtune=native -fgraphite-identity -O3 -Wall -Wl,--as-needed -Wl,--build-id=sha1 -Wl,--enable-new-dtags -Wl,--hash-style=gnu -Wl,-O2 -Wl,-z,now -Wl,-z,relro -falign-functions=32 -fasynchronous-unwind-tables -fdevirtualize-at-ltrans -floop-nest-optimize -fno-math-errno -fno-semantic-interposition -fno-stack-protector -fno-trapping-math -ftree-loop-distribute-patterns -ftree-loop-vectorize -ftree-vectorize -funroll-loops -fuse-ld=bfd -fuse-linker-plugin -malign-data=cacheline -fno-plt -mtls-dialect=gnu2 -Wl,-sort-common -pipe -I/usr/include/python3.8/ -fcommon"
export FFLAGS="$CFLAGS"

unset LD_AS_NEEDED
BuildTools() {
    pushd tools/perf
    make V=1 NO_GTK2=1 WERROR=0 PYTHON=/usr/bin/python3 PYTHON_CONFIG=/usr/bin/python3-config %{?sparse_mflags}
    popd
    pushd tools/power/x86/turbostat
    make
    popd
    pushd tools/power/x86/intel-speed-select
    make
    popd
    pushd tools/power/x86/x86_energy_perf_policy
    make
    popd
}

BuildHyperVDaemons() {
    pushd tools/hv
    make
    popd
}

BuildTools
BuildHyperVDaemons

%install
export GCC_IGNORE_WERROR=1
export CFLAGS="-g1 -O3 -Wl,-z -Wl,now -Wl,-z -Wl,relro -Wl,-z,max-page-size=0x1000 -march=native -mtune=native -fgraphite-identity -O3 -Wall -Wl,--as-needed -Wl,--build-id=sha1 -Wl,--enable-new-dtags -Wl,--hash-style=gnu -Wl,-O2 -Wl,-z,now -Wl,-z,relro -falign-functions=32 -fasynchronous-unwind-tables -fdevirtualize-at-ltrans -floop-nest-optimize -fno-math-errno -fno-semantic-interposition -fno-stack-protector -fno-trapping-math -ftree-loop-distribute-patterns -ftree-loop-vectorize -ftree-vectorize -funroll-loops -fuse-ld=bfd -fuse-linker-plugin -malign-data=cacheline -fno-plt -mtls-dialect=gnu2 -Wl,-sort-common -pipe -I/usr/include/python3.8/ -fcommon"
export CXXFLAGS="-g1 -O3  -Wl,-z,max-page-size=0x1000 -march=native -mtune=native -fgraphite-identity -O3 -Wall -Wl,--as-needed -Wl,--build-id=sha1 -Wl,--enable-new-dtags -Wl,--hash-style=gnu -Wl,-O2 -Wl,-z,now -Wl,-z,relro -falign-functions=32 -fasynchronous-unwind-tables -fdevirtualize-at-ltrans -floop-nest-optimize -fno-math-errno -fno-semantic-interposition -fno-stack-protector -fno-trapping-math -ftree-loop-distribute-patterns -ftree-loop-vectorize -ftree-vectorize -funroll-loops -fuse-ld=bfd -fuse-linker-plugin -malign-data=cacheline -fno-plt -mtls-dialect=gnu2 -Wl,-sort-common -pipe -I/usr/include/python3.8/ -fcommon"
export LDFLAGS="-g1 -O3 -Wl,-z -Wl,now -Wl,-z -Wl,relro -Wl,-z,max-page-size=0x1000 -march=native -mtune=native -fgraphite-identity -O3 -Wall -Wl,--as-needed -Wl,--build-id=sha1 -Wl,--enable-new-dtags -Wl,--hash-style=gnu -Wl,-O2 -Wl,-z,now -Wl,-z,relro -falign-functions=32 -fasynchronous-unwind-tables -fdevirtualize-at-ltrans -floop-nest-optimize -fno-math-errno -fno-semantic-interposition -fno-stack-protector -fno-trapping-math -ftree-loop-distribute-patterns -ftree-loop-vectorize -ftree-vectorize -funroll-loops -fuse-ld=bfd -fuse-linker-plugin -malign-data=cacheline -fno-plt -mtls-dialect=gnu2 -Wl,-sort-common -pipe -I/usr/include/python3.8/ -fcommon"
export FFLAGS="$CFLAGS"

InstallTools() {
    pushd tools/perf
    %make_install prefix=/usr WERROR=0 DESTDIR=%{buildroot} mandir=/usr/share/man PYTHON=/usr/bin/python3 PYTHON_CONFIG=/usr/bin/python3-config  
	pushd Documentation
	make man WERROR=0 DESTDIR=%{buildroot} mandir=/usr/share/man PYTHON=/usr/bin/python3 PYTHON_CONFIG=/usr/bin/python3-config 
	make WERROR=0 DESTDIR=%{buildroot} mandir=/usr/share/man PYTHON=/usr/bin/python3 PYTHON_CONFIG=/usr/bin/python3-config install
	popd
    popd
    pushd tools/power/x86/turbostat
    %make_install prefix=/usr
    popd
    pushd tools/power/x86/intel-speed-select
    %make_install prefix=/usr
    popd
    pushd tools/kvm/kvm_stat
	make
	make INSTALL_ROOT=%{buildroot} install
    popd
    pushd tools/power/x86/x86_energy_perf_policy
    %make_install prefix=/usr
    popd
}

InstallHyperVDaemons() {
    pushd tools/hv
    mkdir -p %{buildroot}/usr/bin
    cp hv_fcopy_daemon %{buildroot}/usr/bin
    cp hv_kvp_daemon %{buildroot}/usr/bin
    cp hv_vss_daemon %{buildroot}/usr/bin
    popd
}

InstallTools
InstallHyperVDaemons

# Move bash-completion
mkdir -p %{buildroot}/usr/share/bash-completion/completions
mv %{buildroot}/etc/bash_completion.d/perf %{buildroot}/usr/share/bash-completion/completions/perf
rmdir %{buildroot}/etc/bash_completion.d
rmdir %{buildroot}/etc
mkdir -p %{buildroot}/usr/share

chmod 0644 %{buildroot}/usr/share/man/man8/*

%files
/usr/bin/trace
/usr/bin/perf
/usr/bin/intel-speed-select
/usr/libexec/perf-core
/usr/lib64/traceevent/plugins/
/usr/share/bash-completion/completions/*
/usr/bin/turbostat
/usr/share/man/man8/turbostat.8
/usr/share/man/man1
/usr/share/doc/perf-tip/tips.txt
/usr/bin/kvm_stat
/usr/bin/x86_energy_perf_policy
/usr/share/man/man8/x86_energy_perf_policy.8
/usr/share/perf-core/strace/groups/file
/usr/share/perf-core/strace/groups/string
/usr/lib/perf/examples/bpf/5sec.c
/usr/lib/perf/examples/bpf/augmented_syscalls.c
/usr/lib/perf/examples/bpf/empty.c
/usr/lib/perf/examples/bpf/hello.c
/usr/lib/perf/examples/bpf/sys_enter_openat.c
/usr/lib/perf/include/bpf/bpf.h
/usr/lib/perf/include/bpf/stdio.h
/usr/lib/perf/examples/bpf/augmented_raw_syscalls.c
/usr/lib/perf/examples/bpf/etcsnoop.c
/usr/lib/perf/include/bpf/linux/socket.h
/usr/lib/perf/include/bpf/pid_filter.h
/usr/lib/perf/include/bpf/unistd.h

%files hyperv
/usr/bin/hv_fcopy_daemon
/usr/bin/hv_kvp_daemon
/usr/bin/hv_vss_daemon
