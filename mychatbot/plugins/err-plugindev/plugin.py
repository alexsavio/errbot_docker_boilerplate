# -*- coding: utf-8 -*-
"""
Errbot plugin boilerplate.
"""
import os.path as path
from itertools import chain

from everett.manager import ConfigManager, ConfigDictEnv, ConfigEnvFileEnv
from errbot import BotPlugin, botcmd, arg_botcmd


# put here the name of the plugin, to be able to find configuration variables.
PLUGIN_CONFIG_NAME = 'err-plugindev'

CONFIG_FILEPATH_CHOICES = [path.join(path.dirname(__file__), '{}.env'),
                           '~/.{}/config.env',
                           '/etc/errbot/{}.env',
                           '/etc/errbot/{}/err-rss.env',
                           '/etc/errbot/{}/config.env',
                           ]
CONFIG_FILEPATH_CHOICES = [f.format(PLUGIN_CONFIG_NAME) for f in
                           CONFIG_FILEPATH_CHOICES]


CONFIG_TEMPLATE = {'START_DATE': '01/01/2017',  # format: DD/MM/YYYY
                   'INTERVAL': 5*60,  # refresh time in seconds#
                   'ENTRY_FORMAT_FUNCTION': '',
                   }


def read_config():
    """ Return an everett.ConfigManager or a dict with the configuration values
    obtained from the .env files and/or the CONFIG_TEMPLATE."""
    config = ConfigManager([ConfigEnvFileEnv(CONFIG_FILEPATH_CHOICES),
                            ConfigDictEnv(CONFIG_TEMPLATE),
                            ])
    ##  This will build a dict from the configmanager with the Keys
    ##  from CONFIG_TEMPLATE. The problem is that the ConfigManager does not
    ##  know the types of the variables.
    return {config(key, default=val, parser=type(val))
            for key, val in CONFIG_TEMPLATE.items()}

    # This will directly return the ConfigManager. The plugin will have
    # to use the self.config as an Everett.ConfigManager object, not a dict.
    # return config


class PluginDev(BotPlugin):
    """Errbot plugin boilerplate."""

    def configure(self, configuration):
        if configuration is None or not configuration:
            config = read_config()
        else:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        super().configure(config)

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def activate(self):
        super().activate()

    def deactivate(self):
        super().deactivate()

    @botcmd
    def dev_hello(self, message, args):
        """Return a hello!"""
        return 'Hello!'
