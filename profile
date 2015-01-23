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

CFLAGS="-O2 -g2 -feliminate-unused-debug-types  -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=32 -Wformat -Wformat-security -Wl,--copy-dt-needed-entries -falign-functions=32 -Wno-error -m64 -march=core2 -msse4.2  -mtune=native  -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -O2 -fipa-cp-clone -ftree-vectorize  -Wp,-D_REENTRANT -ftree-loop-distribute-patterns -Wl,-z -Wl,now -Wl,-z -Wl,relro"
CXXFLAGS="$CFLAGS"
if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/* ; do
    . $i
  done
  unset i
fi
export PATH PS1 OPIEDIR QPEDIR QTDIR EDITOR TERM CFLAGS CXXFLAGS

umask 022

