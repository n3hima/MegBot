##
#This file is part of MegBot.
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

import time
import Libraries.store as store

def main(connection):
    """
    Looks for the last time the user spoke and reports it.
    """
    if not Info.args:
        Channel.send(u"Please specify a user")
        return

    if Info.args[0] == connection.settings["nick"]:
        Channel.send(u"No I haven't seen myself, I'm all 1s and 0s")
        return

    try:
        seen = store.Store("Seen")
    except IOError:
        seen = store.Store("Seen", {})

    try:
        record = seen[connection.name][Info.channel][unicode(Info.args[0])]
        Channel.send(u"%s said \"%s\" %s", 
            Info.args[0], 
            record["msg"].strip(), 
            Helper.HumanTime(Helper.convertToTime(record["time"])).lower()
        )
    except KeyError:
        Channel.send("Haven't seen %s." % Info.args[0])

def on_PRIVMSG(connection, info):
    """
    Logs this speach.
    """
    try:
        seen = store.Store("Seen")
    except IOError:
        seen = store.Store("Seen", {})
    # there's got to be a better way fo doing this... it looks so ugly :(
    if connection.name in seen:
        if info.channel in seen[connection.name]:
            seen[connection.name][info.channel][info.nick] = {"msg":info.message, "time":time.time()}
        else:
            #new channel
            seen[connection.name][info.channel] = {info.nick: {"msg":info.message, "time":time.time()}}
    else:
        #new connection etc.
        seen[connection.name] = {info.channel: {info.nick: {"msg":info.message, "time":time.time()}}}
    seen.save()


def init(connection):
    eventID = 'seenEvent'
    info = connection.libraries["IRCObjects"].Info()

    # this will peform an event on privmsg.
    info.action = "PRIVMSG"
    event = connection.core["Corehandler"].IRCEvent(info, on_PRIVMSG, eventID)
    connection.handler.register_event(event)


def unload(connection):
    eventID = 'seenEvent'
    connection.handler.unregister_event(eventID)

help = u"Tells you the last time a specified nick spoke."
