Name:           filesystem
Version:        3.0.14
Release:        58
License:        GPL-2.0
Summary:        Base files for the system
Url:            https://01.org/
Group:          base
Source1:        nsswitch.conf
Source2:        profile
Source3:        dot.bashrc
Source4:        dot.profile
Source5:        os-release
Provides: /bin/sh  /bin/bash

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
for d in \
 /boot \
 /dev \
 %{_sysconfdir} \
 /mnt \
 /home \
 /proc \
 /root \
 /run \
 /sys \
 /usr \
 /usr/bin \
 /usr/share/doc/filesystem-3.0.14 \
 /usr/games \
 /usr/include \
 /usr/lib64 \
 /usr/lib \
 /usr/lib/debug \
 /usr/src/debug \
 /usr/share \
 /usr/share/common-licenses \
 /usr/share/defaults/skel \
 /usr/share/dict \
 /usr/share/info \
 /usr/share/man \
 /usr/share/misc \
 /var/log/journal \
 /usr/src \
 %{_localstatedir} \
 %{_localstatedir}/lib \
 %{_localstatedir}/log \
 %{_localstatedir}/spool \
 /media ; do
        install -m 0755 -d %{buildroot}$d
done


# systemd
mkdir -p ${RPM_BUILD_ROOT}/var/empty
mkdir -p ${RPM_BUILD_ROOT}/var/log/journal
mkdir -p ${RPM_BUILD_ROOT}/var/cache/ldconfig
mkdir -p  ${RPM_BUILD_ROOT}/usr/share/defaults/etc

for d in /tmp %{_localstatedir}/tmp; do
        install -m 1777 -d %{buildroot}$d
done

ln -snf ../run %{buildroot}%{_localstatedir}/run
ln -snf ../run/lock %{buildroot}%{_localstatedir}/lock

# usr migration
ln -sfv usr/bin %{buildroot}/bin
ln -sfv usr/bin %{buildroot}/sbin
ln -sfv usr/lib64 %{buildroot}/lib64
ln -sf usr/lib %{buildroot}/lib
ln -sf bin %{buildroot}%{_prefix}/sbin
#ln -sf usr/bin/bash  %{buildroot}/bin/sh

install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/defaults/etc/nsswitch.conf
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/defaults/etc/profile
install -m 0755 %{SOURCE3} %{buildroot}%{_datadir}/defaults/skel/.bashrc
install -m 0755 %{SOURCE4} %{buildroot}%{_datadir}/defaults/skel/.profile
# os-release
install -m 644 %{SOURCE5} %{buildroot}%{_prefix}/lib



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
%dir /tmp
%dir /usr
%dir %{_prefix}/bin
%dir %{_datadir}/doc/filesystem-3.0.14
%dir %{_prefix}/games
%dir %{_prefix}/include
%dir %{_prefix}/lib64
%dir %{_prefix}/lib
%dir %{_prefix}/lib/debug
%dir %{_prefix}/share
%dir %{_prefix}/src
%dir %{_prefix}/src/debug
%dir %{_datadir}/common-licenses
%dir %{_datadir}/dict
%dir %{_datadir}/info
%dir %{_datadir}/man
%dir %{_datadir}/misc
%dir %{_localstatedir}
%dir %{_localstatedir}/tmp
%dir %{_localstatedir}/lib
%dir %{_localstatedir}/log
%dir %{_localstatedir}/spool
%dir /var/log/journal
%dir /var/cache/ldconfig

%dir /media
# symlinks...
/bin
/lib64
/lib
/sbin
%{_prefix}/sbin
#/usr/bin/sh

%{_localstatedir}/lock
%{_localstatedir}/run
%{_prefix}/lib/os-release
%{_datadir}/defaults
