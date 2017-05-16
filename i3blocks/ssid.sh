#!/bin/bash
#########################################################################
# File Name: ssid.sh
# Author: Fu Jingyuan
# E-mail: jyfu2_12@outlook.com
# Created Time: 2017-04-09 17:37:35
#########################################################################
SSID_NAME=$(iwgetid -r)

# You can put any urgent name so the block will give warning
# if a network with this name is used, like public wifi or alike.
# You can separate multiple values with \|
URGENT_VALUE=""

if [[ "${SSID_NAME}" != "" ]]; then
  echo " "
 # echo "${SSID_NAME}"
 # echo ""

  if [[ "${URGENT_VALUE}" != "" ]] && [[ $(echo "${SSID_NAME}" | grep -we "${URGENT_VALUE}") != "" ]]; then
    exit 33
  fi
fi
