#!/bin/bash
file=${1//[^a-zA-Z0-9\.\-\/]/}

# step 1: the main binary itself
file "/usr/lib/debug/$file.debug" > /dev/null
# step 2: all the libs it depends on
libs=`ldd $file | cut -f2 -d">"  | cut -f1 -d"(" | grep -v vdso`
for i in $libs; do
	ll=`readlink -f $i`
	file "/usr/lib/debug/$ll.debug" > /dev/null
done

# step 3
pid=`pidof $file`
libs=`cat /proc/$pid/maps | cut -c74- | grep -v deleted | grep -v "\[" | sort | uniq`
for i in $libs; do
	ll=`readlink -f $i`
	file "/usr/lib/debug/$ll.debug" > /dev/null
done

# sleep 3 seconds to let all downloads finish

sleep 3	
