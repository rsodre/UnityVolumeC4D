#!/bin/sh

# Delete C4D attributes cache
# Find your folder in Edit > Preferences > Open Preferences folder
export PREFERENCES_FOLDER="$HOME/Library/Preferences/MAXON/CINEMA 4D R20_7DE41E5A"
rm -f "$PREFERENCES_FOLDER/prefs/symbolcache"

# Copy plugin to C4D
#export PLUGINS_FOLDER="/Applications/MAXON/CINEMA 4D R20/plugins"
#rm -rf "$PLUGINS_FOLDER/UnityVolume"
#cp -R ../UnityVolume "$PLUGINS_FOLDER"
