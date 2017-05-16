#!/bin/bash
#########################################################################
# File Name: wifi.sh
# Author: Fu Jingyuan
# E-mail: jyfu2_12@outlook.com
# Created Time: 2017-04-09 17:18:27
#########################################################################
#!/bin/bash


INTERFACE="${BLOCK_INSTANCE:-wlp3s0}"

#------------------------------------------------------------------------

# As per #36 -- It is transparent: e.g. if the machine has no battery or wireless
# connection (think desktop), the corresponding block should not be displayed.
[[ ! -d /sys/class/net/${INTERFACE}/wireless ]] ||
    [[ "$(cat /sys/class/net/$INTERFACE/operstate)" = 'down' ]] && exit

#------------------------------------------------------------------------

QUALITY=$(grep $INTERFACE /proc/net/wireless | awk '{ print int($3 * 100 / 70) }')

#------------------------------------------------------------------------

echo $QUALITY% # full text
echo $QUALITY% # short text

# color
if [[ $QUALITY -ge 70 ]]; then
    echo " "
elif [[ $QUALITY -ge 60 ]]; then
    echo " "
elif [[ $QUALITY -ge 50 ]]; then
    echo " "
elif [[ $QUALITY -ge 40 ]]; then
    echo " " 
fi
