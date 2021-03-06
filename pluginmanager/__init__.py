import imp
import os


class Plugin(object):
    data = None
    plugin = None
    plugin_object = None

    def __init__(self, data):
        self.data = data


class PluginManager(object):

    plugin_folder = "./plugins"
    main_module = "__init__"
    plugins = None

    def get_plugins(self):
        for i in os.listdir(self.plugin_folder):
            if i.endswith(".pyc"):
                continue

            if not os.path.isdir(os.path.join(self.plugin_folder, i)):
                continue

            directory_listing = os.listdir(os.path.join(self.plugin_folder, i))

            if ("%s.py" % self.main_module) in directory_listing:
                location = os.path.join(self.plugin_folder, i)
                info = imp.find_module(self.main_module, [location])
                self.plugins.append(Plugin({"name": i, "info": info}))

    def load_plugin(self, plugin):
        return imp.load_module(self.main_module, *plugin.data["info"])

    def load_plugins(self, **kwargs):
        for plugin in self.plugins:
            plugin.plugin = self.load_plugin(plugin)
            plugin.plugin_object = plugin.plugin.Plugin(**kwargs)

    def __init__(self):
        self.plugins = []
