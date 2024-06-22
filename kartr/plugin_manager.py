import importlib

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugin(self, name):
        try:
            module = importlib.import_module(f"kartr.plugins.{name}")
            self.plugins[name] = module.Plugin()
        except ImportError:
            print(f"Failed to load plugin: {name}")

    async def execute(self, plugin_name, command):
        if plugin_name not in self.plugins:
            self.load_plugin(plugin_name)
        if plugin_name in self.plugins:
            return await self.plugins[plugin_name].execute(command)
        else:
            return f"Plugin not found: {plugin_name}"
