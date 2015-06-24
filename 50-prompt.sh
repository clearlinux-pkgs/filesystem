endchar="\$"
if [ "$UID" = "0" ]; then
    endchar="#"
fi

# Blue
BG="\[\e[38;5;39m\]"
# RGBA index:
#BG="\[\e[38;2;255;142;58m\]"

# Orange
FG="\[\e[38;5;208m\]"
# RGBA index:
#FG="\[\e[38;2;0;174;255m\]"

export PS1="$BG\u\[\e[0m\]@$FG\H ${BG}\w ${BG}$endchar \[\e[0;0m\]"
if [ "${TERM:0:5}" = "xterm" ]; then
  export PS1="\[\e]2;\u@\H :: \w\a\]$PS1"
fi

shopt -s checkwinsize 
