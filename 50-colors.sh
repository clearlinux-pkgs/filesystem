# ls colors
alias ls='ls --color=auto'
if [ -f "$HOME/.dircolors" ]; then
  eval `dircolors -b "$HOME/.dircolors"`
elif [ -f "/etc/dircolors" ]; then
  eval `dircolors -b "/etc/dircolors"`
elif [ -f "/usr/share/defaults/etc/LS_COLORS" ]; then
  eval $( dircolors -b /usr/share/defaults/etc/LS_COLORS )
fi

# GCC diagnostics/colors
export GCC_COLORS="error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01"
