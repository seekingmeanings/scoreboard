"""
this file manages the plugins and the distribution of content
"""


class Plugin:
    def __init__(self, plugin, plugin_conf, resources):
        self.external_resources = resources

        self._plugin = None


# from time plugin
# TODO: make this an actual plugin class and this an instance
#class Plugin:
#    def __init__(self, plugin_conf, resources):
#        self.external_resources = resources
#
#        # init the plugin
#        self._plugin = TimePlugin(
#            self.external_resources['board'],
#            self.external_resources['config']['plugins']['p']['time']['config_file']
#        )
#
#        self.external_resources['time'] = self._plugin