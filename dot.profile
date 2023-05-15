# ~/.profile: executed by Bourne-compatible login shells.
me=${BASH_SOURCE[0]//\//_}; me=${me//./_}; if [[ ${SOURCED[${me}]} == "yes" ]]; then return; else declare -A SOURCED; SOURCED[${me}]=yes; fi # Only load once

if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi

# path set by /etc/profile
# export PATH

# mesg n
