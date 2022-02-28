from dynaconf import Dynaconf

settings = Dynaconf(envvar_prefix="DYNACONF",
                    settings_files=['conf/dev.toml', 'conf/prod.toml'],
                    environments=True)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
