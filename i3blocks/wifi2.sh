#!/bin/bash
# Copyright (C) 2014 Alexander Keller <github@nycroth.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#------------------------------------------------------------------------

INTERFACE="${BLOCK_INSTANCE:-wlp3s0}"
SIGNAL=1

#------------------------------------------------------------------------

if [[ $BLOCK_BUTTON -eq 1 ]]; then
    bash -c "wicd-client -n > /dev/null 2>&1 && pkill -RTMIN+$SIGNAL i3blocks" &
fi

# As per #36 -- It is transparent: e.g. if the machine has no battery or wireless
# connection (think desktop), the corresponding block should not be displayed.
if [[ ! -d /sys/class/net/${INTERFACE}/wireless ]] || [[ "$(cat /sys/class/net/$INTERFACE/operstate)" = 'down' ]]; then
  
    #printf " NC\n NC\n#660000"
    printf " WIFI off\n WIFI off\n#b60000"
    if [[ $BLOCK_BUTTON -eq 1 ]]; then
    	tilda -c "nmcli_dmenu" &
    fi
    exit
fi

#------------------------------------------------------------------------

QUAL=$( iwconfig $INTERFACE | grep "Link Quality" | awk '{ print $2}' | awk -F\= '{ print $2 }')
MAX_QUAL=$( echo $QUAL | awk -F/ '{ print $2 }')
CUR_QUAL=$( echo $QUAL | awk -F/ '{ print $1 }')
QUALITY=$(( $CUR_QUAL*100/$MAX_QUAL ))
SSID=$( iwconfig $INTERFACE | grep "ESSID:" | awk -F\" '{ print $2}')

#------------------------------------------------------------------------

echo   $SSID $QUALITY% # full text
echo $SSID  # short text

# color
if [[ $QUALITY -ge 80 ]]; then
    echo "#00FF00"
elif [[ $QUALITY -lt 80 ]]; then
    echo "#FFF600"
elif [[ $QUALITY -lt 60 ]]; then
    echo "#FFAE00"
elif [[ $QUALITY -lt 40 ]]; then
    echo "#FF0000"
fi

if [[ $BLOCK_BUTTON -eq 1 ]]; then
	tilda -c "nmcli_dmenu" &
fi
