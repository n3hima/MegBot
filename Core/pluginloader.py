##
#   This file is part of MegBot.
#
#   MegBot is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   MegBot is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with MegBot.  If not, see <http://www.gnu.org/licenses/>.
##

"""This is to load plugins, if you leave plugin as the default (None)
it will go out and try and load them all. It doesn't return anything.
Instead of returning anything it adds the plugins directly onto the
connection by access through the connection parameter passed to main.
"""
from traceback import format_exc
import glob
import imp
import os
import logging

def main(connection, plugin=None):
    """
    This will load plugins, if plugin is left as the default (None) then
    it will look in Plugins/ (or what's specified in the config under
    the dict path). if it's specified it will only load that specific plugin.
    This will also add the Server, Helper and Web instances to the bots
    """
    if plugin:
        if plugin in connection.plugins and "unload" in dir(connection.plugins[plugin][0]):
            connection.plugins[plugin][0].unload(connection)
        plugin_path = connection.config[u"paths"][u"plugin"] + plugin + ".py"
        if not os.path.isfile(plugin_path):
            return (False, "Can't find plugin")
        try:
            mtime = os.stat(plugin_path).st_mtime
            
            # check if it's the same copy?
            if plugin in connection.plugins and connection.plugins[plugin][1] == mtime:
                return (False, "Plugin already loaded.")

            # load the plugin
            loaded_plugin = imp.load_source(plugin, plugin_path)
            connection.plugins[plugin] = (loaded_plugin, mtime)
            connection.Server = connection.server
            if "init" in dir(connection.plugins[plugin][0]):
                connection.plugins[plugin][0].init(connection)
            return (True, "")
        except:
            return (False, "Oh no, something went wrong,", format_exc())

    else:
        for plugfi in glob.glob(connection.config[u"paths"][u"plugin"] + "*.py"):
            name = os.path.splitext(os.path.basename(plugfi))[0]
            if name == '__init__':
                continue
            result = main(connection, name)
            if not result[0]:
                if len(result) == 3:
                    logging.error("Plugin load failed. %s", result[2])
                continue

            plugin = connection.plugins[name][0]
            plugin.Server = connection.server
            plugin.Helper = connection.libraries["IRCObjects"].L_Helper()
            plugin.Web = connection.libraries["IRCObjects"].L_Web(connection)
            plugin.Format = connection.libraries["IRCObjects"].L_Format
            if "init" in dir(connection.plugins[name]):
                connection.plugins[name][0].init(connection)
