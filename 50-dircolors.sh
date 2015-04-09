alias ls='ls --color=auto'
if [ -f "$HOME/.dircolors" ]; then
  eval `dircolors -b "$HOME/.dircolors"`
else
  if [ -f "/etc/dircolors" ]; then
    eval `dircolors -b "/etc/dircolors"`
  fi
fi
