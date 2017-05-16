#!/bin/bash

while true; do
  find ~/Desktop/wallpaper -type f \
    -name '*.jpg' -print0 | shuf -n1 -z | xargs -0 feh --bg-scale
  sleep 10m
done
