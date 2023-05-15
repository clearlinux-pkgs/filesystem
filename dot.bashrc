me=${BASH_SOURCE[0]//\//_}; me=${me//./_}; if [[ ${SOURCED[${me}]} == "yes" ]]; then return; else declare -A SOURCED; SOURCED[${me}]=yes; fi # Only load once

# Use global profile when available
if [ -f /usr/share/defaults/etc/profile ]; then
	. /usr/share/defaults/etc/profile
fi
