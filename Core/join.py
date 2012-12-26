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

def main(connection, channel):
    """ Joins channel specified """
    if connection.libraries:
        connection.channels[channel] = connection.libraries["IRCObjects"].L_Channel(connection, channel)
        connection.channels[channel].__setuphooks__(connection)
    connection.core["Coreraw"].main(connection, "JOIN %s" % channel)
