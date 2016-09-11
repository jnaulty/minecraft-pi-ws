#!/bin/bash

mc=$(ps aux | grep minecraft-pi | grep -v grep)
check_mc=$?

if [ ${check_mc} = "0" ]
then
    echo "Minecraft-pi is running"
else
    echo "Must start minecraft-pi game"
    exit 1
fi

echo "starting heart-race counterstrike"
python counterstrike.py
