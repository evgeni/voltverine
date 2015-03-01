voltverine
==========
Shutdown your machine when certain conditions are met.

configuration
-------------
In theory you should not need a configuration in many cases. Yet, not
all plugins will work properly without a configuration.

`voltverine` uses a YAML file for its configuration, with currently only
two possible entries: `action` and `plugins`. While `action` is a
literal string, representing an action from `voltverine.actions` to be
executed, `plugins` can be either a list or a hash of plugins from
`voltverine.plugins`. See the following examples:

    ---
    action: LogindPoweroff
    plugins:
      - LogindSessions
      - LogindInhibitors

This will set the `action` to `LogindPoweroff` and enable the
`LogindSessions` and `LogindInhibitors` plugins, without further
configuration of them.

    ---
    plugins:
      NoShutdownFile:
        filename: /some/path

This does not set an `action` and `voltverine` will use the default
action (`LogindPowerof`). This also enables the `NoShutdownFile` plugin
and configures it to watch for a file called `/some/path`.
