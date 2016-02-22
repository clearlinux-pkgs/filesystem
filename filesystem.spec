Name:           filesystem
Version:        3.0.14
Release:        96
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
Source9:	profile.i386
Provides: /bin/bash
Provides: /bin/sh
Provides: /bin/zsh
Provides: /bin/ksh
BuildRequires: /usr/bin/systemd-tmpfiles

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
	[[ $T == "L" ]] && ln -sf $L %{buildroot}$P; \
done < %{buildroot}/usr/lib/tmpfiles.d/filesystem.conf

# See coreutils %post, host yum puts a pid file there.
rm -f %{buildroot}%{_localstatedir}/run

mkdir -p %{buildroot}/usr/share/defaults/etc
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/defaults/etc/nsswitch.conf
%ifarch i386
install -m 0644 %{SOURCE9} %{buildroot}%{_datadir}/defaults/etc/profile
ln -s /usr/lib64/ld-2.22.so %{buildroot}/usr/lib/ld-linux.so.2
%else
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/defaults/etc/profile
%endif
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/defaults/skel/.bashrc
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/defaults/etc/bash.bashrc
install -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/defaults/skel/.profile
# os-release
install -m 644 %{SOURCE5} %{buildroot}%{_prefix}/lib

install -m 644 -D %{SOURCE6} %{buildroot}%{_datadir}/defaults/etc/profile.d/50-prompt.sh
install -m 644 -D %{SOURCE7} %{buildroot}%{_datadir}/defaults/etc/profile.d/50-colors.sh

# inputrc
install -m 0644 %{SOURCE8} %{buildroot}%{_datadir}/defaults/etc/inputrc

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
%dir %{_sysconfdir}
%dir /mnt
%dir /home
%dir /proc
%dir %attr(0700, root, root) /root
%dir /run
%dir /sys
%dir /srv
%dir %attr(1777, root, root) /tmp
%dir /usr
%dir %{_prefix}/bin
%dir %{_prefix}/include
%dir %{_prefix}/lib64
%dir %{_prefix}/lib
%dir %{_prefix}/lib/debug
%dir %{_prefix}/share
%dir %{_prefix}/src
%dir %{_prefix}/src/debug
%dir %{_datadir}/info
%dir %{_datadir}/man
%dir %{_localstatedir}
%dir %attr(1777, root, root) %{_localstatedir}/tmp
%dir %{_localstatedir}/lib
%dir %{_localstatedir}/log
%dir %{_localstatedir}/cache
%dir %{_localstatedir}/spool

%dir /media
# symlinks...
/bin
/lib64
/lib
/sbin
%{_prefix}/sbin
#/usr/bin/sh

%{_localstatedir}/lock
%{_prefix}/lib/os-release
%{_prefix}/lib/tmpfiles.d/filesystem.conf
%{_datadir}/defaults
%ifarch i386
/usr/lib/ld-linux.so.2
%endif
