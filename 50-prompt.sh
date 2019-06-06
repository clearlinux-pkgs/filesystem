# Set prompt and title (for interactive shells only)
if [ "$(expr $- : '.*i')" -ne 0 ]; then

  # this works for sh and bash
  if [ -z "$ZSH_VERSION" ]; then
    __stateless_prompt() {
      local EXIT="$?"                     # exit code of last command
      local BLUE="\[\e[38;5;39m\]"
      local RED="\[\e[31m\]"
      local ORANGE="\[\e[38;5;208m\]"
      local WHITE="\[\e[0m\]"
      # endchar and username
      local endchar="\$${WHITE}"          # $ for non-root users
      local username="${BLUE}\u${WHITE}"  # blue(39) for non-root
      if [ "$UID" = "0" ]; then
        endchar="#${WHITE}"               # # for root user
        username="${RED}\u${WHITE}"       # red for root
      fi
      if [ "$EXIT" -eq 0 ]; then
        endchar="${WHITE}$endchar"        # White enchar as default
      else
        endchar="${RED}$endchar"          # Red endchar for error
      fi
      # hostname in orange
      local host="${ORANGE}\H${WHITE}"
      # current directory in blue(39)
      local dir="${BLUE}\w${WHITE}"
      # set prompt
      export PS1="${username}@${host} ${dir} ${endchar} "
      # set window title for xterm
      if [ "${TERM:0:5}" = "xterm" ]; then
        export PS1="\[\e]2;\u@\H :: \w\a\]$PS1"
      fi
    }

    export PROMPT_COMMAND=__stateless_prompt

  else
    # this works for zsh
    __stateless_prompt() {    # set prompt
      # endchar
      # use red if last command has non-zero exit
      # use # for root and $ for non-root users
      local root_endch="%(?.#.%F{red}#%f)"
      local other_endch="%(?.$.%F{red}$%f)"
      local endchar="%(#.${root_endch}.${other_endch})"
      # use red for root and blue(39) for non-root users
      local username="%F{%(#.red.39)}%n%f"
      # hostname in orange
      local host="%F{208}%m%f"
      # current directory in blue(39)
      local dir="%F{39}%~%f"
      export PS1="${username}@${host} ${dir} ${endchar} "
    }
    __stateless_title () {    # for xterm, set window title
      if [ "${TERM:0:5}" = "xterm" ]; then
        print -Pn "\e]2;%n@%m :: %~\a"
      fi
    }
    autoload -Uz add-zsh-hook
    add-zsh-hook preexec __stateless_prompt
    add-zsh-hook precmd __stateless_title
  fi
fi
