Name:           filesystem
Version:        3.0.14
Release:        5
License:        GPL-2.0
Summary:        Base files for the system
Url:            https://01.org/
Group:          base
Source0:        rotation
Source1:        nsswitch.conf
Source2:        motd
Source3:        inputrc
Source4:        host.conf
Source5:        profile
Source6:        shells
Source9:        issue.net
Source10:       issue
Source11:       dot.bashrc
Source12:       dot.profile
Source13:       passwd
Source14:       group
Source15:       os-release
Source16:       shadow
Source17:       hosts
BuildArch:      noarch

%description
Base files for the system.

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
 %{_sysconfdir}/default \
 %{_sysconfdir}/skel \
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
 /usr/sbin \
 /usr/share \
 /usr/share/common-licenses \
 /usr/share/dict \
 /usr/share/info \
 /usr/share/man \
 /usr/share/misc \
 /usr/src \
 %{_localstatedir} \
 %{_localstatedir}/lib \
 %{_localstatedir}/log \
 %{_localstatedir}/spool \
 /media ; do
        install -m 0755 -d %{buildroot}$d
done

for d in /tmp %{_localstatedir}/tmp; do
        install -m 1777 -d %{buildroot}$d
done

# ln -snf ../run %{buildroot}%{_localstatedir}/run
ln -snf ../run/lock %{buildroot}%{_localstatedir}/lock

# Hostname
echo "clr" > %{buildroot}%{_sysconfdir}/hostname

# Issue files
install -m 644 %{SOURCE9} %{SOURCE10} %{buildroot}%{_sysconfdir}
# os-release
install -m 644 %{SOURCE15} %{buildroot}%{_sysconfdir}

rotation=`cat %{SOURCE0}`
if [ "$rotation" != "0" ]; then
        install -m 0644 rotation %{buildroot}%{_sysconfdir}/rotation
fi

# usr migration
ln -sfv usr/bin %{buildroot}/bin
ln -sfv usr/sbin %{buildroot}/sbin
ln -sfv usr/lib64 %{buildroot}/lib
ln -sf usr/lib64 %{buildroot}/lib64
ln -sf lib64 %{buildroot}%{_prefix}/lib

install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/profile
install -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/shells
install -m 0755 %{SOURCE12} %{buildroot}%{_sysconfdir}/skel/.profile
install -m 0755 %{SOURCE11} %{buildroot}%{_sysconfdir}/skel/.bashrc
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/inputrc
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/nsswitch.conf
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/host.conf
install -m 0644 %{SOURCE17} %{buildroot}%{_sysconfdir}/hosts
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/motd

install -m 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/passwd
install -m 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/group

install %{SOURCE16} %{buildroot}%{_sysconfdir}/shadow

ln -sf /proc/mounts %{buildroot}%{_sysconfdir}/mtab

%files
%dir /boot
%dir /dev
%dir %{_sysconfdir}
%dir %{_sysconfdir}/default
%dir %{_sysconfdir}/skel
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
%dir %{_prefix}/sbin
%dir %{_prefix}/share
%dir %{_prefix}/src
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
%dir /media

# symlinks...
/bin
%{_localstatedir}/tmp
/lib64
/lib
%{_prefix}/lib
/sbin

%{_localstatedir}/lock
%{_sysconfdir}/issue
%{_sysconfdir}/os-release
%config %{_sysconfdir}/hostname
%{_sysconfdir}/inputrc
%{_sysconfdir}/motd
%{_sysconfdir}/mtab
%config(noreplace) %{_sysconfdir}/profile
%{_sysconfdir}/nsswitch.conf
%{_sysconfdir}/host.conf
%{_sysconfdir}/hosts
%config %{_sysconfdir}/shells
%{_sysconfdir}/issue.net
%{_sysconfdir}/skel/.profile
%{_sysconfdir}/skel/.bashrc
%config(noreplace) %{_sysconfdir}/passwd
%config(noreplace) %{_sysconfdir}/group
%config(noreplace) %attr(0000,root,root) %{_sysconfdir}/shadow
