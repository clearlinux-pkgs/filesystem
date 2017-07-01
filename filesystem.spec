Name:           filesystem
Version:        3.0.14
Release:        150
License:        GPL-2.0
Summary:        Base files for the system
Url:            https://01.org/
Group:          base
Source0:        filesystem.conf
Source1:        nsswitch.conf
Source2:        profile.x86_64
Source3:        dot.bashrc
Source4:        dot.profile
Source5:        os-release
Source6:        50-prompt.sh
Source7:        50-colors.sh
Source8:        inputrc
Source9:        profile.i386
Source10:       shells
Source11:       locale.conf
Source12:	prime-debuginfo.sh
Source13:	hosts
Provides: /bin/bash
Provides: /bin/sh
Provides: /bin/zsh
Provides: /bin/ksh
BuildRequires: /usr/bin/systemd-tmpfiles


###
### these are the default buildroot deps 
###
BuildRequires : autoconf
BuildRequires : automake
BuildRequires : automake-dev
BuildRequires : binutils
BuildRequires : bzip2
BuildRequires : clr-rpm-config
BuildRequires : coreutils
BuildRequires : diffutils
BuildRequires : gawk
BuildRequires : gcc
BuildRequires : gcc-dev
BuildRequires : gettext
BuildRequires : gettext-bin
BuildRequires : git
BuildRequires : glibc-utils
BuildRequires : grep
BuildRequires : gzip
BuildRequires : hostname
BuildRequires : libc6-dev
BuildRequires : libc6-locale
BuildRequires : libtool
BuildRequires : libtool-dev
BuildRequires : linux-libc-headers
BuildRequires : make
BuildRequires : netbase
BuildRequires : nss-altfiles
BuildRequires : patch
BuildRequires : pigz
BuildRequires : pkg-config
BuildRequires : pkg-config-dev
BuildRequires : rpm-build
BuildRequires : sed
BuildRequires : shadow
BuildRequires : strace
BuildRequires : systemd-libs
BuildRequires : tar
BuildRequires : unzip
BuildRequires : which
BuildRequires : xz

%description
Base files for the system.

%package chroot
Summary: Chroot support for additional filesystem-like setup.

%description chroot
Chroot support for additional filesystem-like setup.

%prep

%build
#Current filesystems package is borked with astray setgid bit
#Fix it, to get this build correct

install -m 0755 -d %{buildroot}
chmod g-s %{buildroot}

%install
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
install -m 0644 %{SOURCE0} %{buildroot}/usr/lib/tmpfiles.d/filesystem.conf
while read T P A U G D L; do \
	[[ $T == "v" ]] && mkdir -p %{buildroot}$P; \
	[[ $T == "d" ]] && mkdir -p %{buildroot}$P; \
	[[ $T == "L+" ]] && ln -sf $L %{buildroot}$P; \
done < %{buildroot}/usr/lib/tmpfiles.d/filesystem.conf

mkdir -p %{buildroot}/usr/share/defaults/etc
install -m 0644 %{SOURCE1} %{buildroot}/usr/share/defaults/etc/nsswitch.conf
%ifarch i386
install -m 0644 %{SOURCE9} %{buildroot}/usr/share/defaults/etc/profile
ln -s /usr/lib64/ld-2.22.so %{buildroot}/usr/lib/ld-linux.so.2
%else
install -m 0644 %{SOURCE2} %{buildroot}/usr/share/defaults/etc/profile
%endif
install -m 0644 %{SOURCE3} %{buildroot}/usr/share/defaults/skel/.bashrc
install -m 0644 %{SOURCE3} %{buildroot}/usr/share/defaults/etc/bash.bashrc
install -m 0644 %{SOURCE4} %{buildroot}/usr/share/defaults/skel/.profile
# os-release
install -m 644 %{SOURCE5} %{buildroot}/usr/lib

install -m 644 -D %{SOURCE6} %{buildroot}/usr/share/defaults/etc/profile.d/50-prompt.sh
install -m 644 -D %{SOURCE7} %{buildroot}/usr/share/defaults/etc/profile.d/50-colors.sh

# inputrc
install -m 0644 %{SOURCE8} %{buildroot}/usr/share/defaults/etc/inputrc

# required for chsh/pam
install -m 00644 %{SOURCE10} %{buildroot}/usr/share/defaults/etc/shells

# set default locale
install -m 0644 %{SOURCE11} %{buildroot}/usr/share/defaults/etc/locale.conf

install -m 0744 %{SOURCE12} %{buildroot}/usr/bin/prime-debuginfo.sh
install -m 0755 %{SOURCE13} %{buildroot}/usr/share/defaults/etc/hosts
chmod a+x  %{buildroot}/usr/bin/prime-debuginfo.sh



%post chroot
# This is mostly mock-chroot support
# Ideally mock should be setting this up
if [ ! -f /etc/machine-id ] && [ -f /var/lib/dbus/machine-id ]
then
    cp /var/lib/dbus/machine-id /etc/machine-id
fi

%files chroot

%files
%dir /boot
%dir /dev
%dir /etc
%dir /mnt
%dir /home
%dir /proc
%dir %attr(0700, root, root) /root
%dir /run
%dir /sys
%dir /srv
%dir %attr(1777, root, root) /tmp
%dir /usr
%dir /usr/bin
%dir /usr/include
%dir /usr/lib64
%dir /usr/lib
%dir /usr/lib32
%dir /usr/lib/debug
%dir /usr/local
%dir /usr/local/share
%dir /usr/share
%dir /usr/src
%dir /usr/src/debug
%dir /usr/share/info
%dir /usr/share/man
%dir /var
%dir %attr(1777, root, root) /var/tmp
%dir /var/lib
%dir /var/log
%dir /var/cache
%dir /var/spool

%dir /media
# symlinks...
/bin
/lib64
/lib
/sbin
/usr/sbin
/var/lock
/var/run
/usr/lib/os-release
/usr/lib/tmpfiles.d/filesystem.conf
/usr/share/defaults
%ifarch i386
/usr/lib/ld-linux.so.2
%endif
/usr/bin/prime-debuginfo.sh
