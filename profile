# /etc/profile: system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

PATH="/usr/local/bin:/usr/bin"
EDITOR="/bin/vi"			# needed for packages like cron
test -z "$TERM" && TERM="xterm"	# Basic terminal capab. For screen etc.

if [ ! -e /etc/localtime ]; then
	TZ="UTC"		# Time Zone. Look at http://theory.uwinnipeg.ca/gnu/glibc/libc_303.html 
				# for an explanation of how to set this to your local timezone.
	export TZ
fi

if [ "$PS1" ]; then
# works for bash and ash (no other shells known to be in use here)
   PS1='\u@\h:\w\$ '
fi

CFLAGS="-O2 -g2 -feliminate-unused-debug-types  -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=32 -Wformat -Wformat-security -Wl,--copy-dt-needed-entries -m64 -march=ivybridge  -mtune=native -fasynchronous-unwind-tables -Wp,-D_REENTRANT -ftree-loop-distribute-patterns -Wl,-z -Wl,now -Wl,-z -Wl,relro -malign-data=abi"
CXXFLAGS="$CFLAGS"
if [ -d /usr/share/defaults/etc/profile.d ]; then
  for i in /usr/share/defaults/etc/profile.d/* ; do
    . $i
  done
  unset i
fi
if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/* ; do
    . $i
  done
  unset i
fi
XDG_CONFIG_DIRS=/usr/share/xdg:/etc/xdg
export PATH PS1 EDITOR TERM CFLAGS CXXFLAGS XDG_CONFIG_DIRS

umask 022

