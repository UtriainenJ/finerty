## user-wide method

To install the Finerty layout, copy the rules and symbols folders into your `$XDG_CONFIG_HOME/xkb/`

Usually (and by default), that is `.config/xkb/`

Reboot if no worky

## I'm feeling lazy
You can also just run the following command to install:
```mkdir -p /tmp/finerty-install && git clone --depth 1 https://github.com/UtriainenJ/finerty.git /tmp/finerty-install && bash /tmp/finerty-install/linux/user-wide/user-install.sh && rm -rf /tmp/finerty-install```

The command and the install script simply pull the repo, place the directories and delete leftovers. Simple enough but nonetheless you probably shouldn't run random scripts off the internet.
