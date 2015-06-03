Name:           filesystem
Version:        3.0.14
Release:        73
License:        GPL-2.0
Summary:        Base files for the system
Url:            https://01.org/
Group:          base
Source0:        filesystem.conf
Source1:        nsswitch.conf
Source2:        profile
Source3:        dot.bashrc
Source4:        dot.profile
Source5:        os-release
Source6:        50-prompt.sh
Source7:        50-colors.sh
Provides: /bin/sh  /bin/bash
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
systemd-tmpfiles --create --root %{buildroot} %{buildroot}/usr/lib/tmpfiles.d/filesystem.conf

# See coreutils %post, host yum puts a pid file there.
rm -f %{buildroot}%{_localstatedir}/run

mkdir -p %{buildroot}/usr/share/defaults/etc
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/defaults/etc/nsswitch.conf
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/defaults/etc/profile
install -m 0755 %{SOURCE3} %{buildroot}%{_datadir}/defaults/skel/.bashrc
install -m 0755 %{SOURCE4} %{buildroot}%{_datadir}/defaults/skel/.profile
# os-release
install -m 644 %{SOURCE5} %{buildroot}%{_prefix}/lib

install -m 644 -D %{SOURCE6} %{buildroot}%{_datadir}/defaults/etc/profile.d/50-prompt.sh
install -m 644 -D %{SOURCE7} %{buildroot}%{_datadir}/defaults/etc/profile.d/50-colors.sh

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
