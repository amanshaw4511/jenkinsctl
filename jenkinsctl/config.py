
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="JENKINS",
    settings_files=['~/.jenkinsctl.yaml', '~/.jenkinsctl.secrets.yaml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
