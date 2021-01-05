#!/usr/bin/env bash
# Authored by Rui.Mu
# Wechat:marey_marey111
#
#
# How to use?
#
# For cse lab machine only.
#
# Windows users, well, have a nice day.
#
# Paste this file to your working directory.
# Use Terminal or iTerm to go to your working directory.
#
# First step:
# run
#   $ chmod +x ./setup_script_for_python.sh
# to make it executable
#
# Second step:
# run
#   $ ./setup_script_for_python.sh
#
# You are free to improve this script, enjoy.
xterm -hold -title "Peer 2" -e "python3 p2p.py init 2 4 5 30" &
xterm -hold -title "Peer 4" -e "python3 p2p.py init 4 5 8 30" &
xterm -hold -title "Peer 5" -e "python3 p2p.py init 5 8 9 30" &
xterm -hold -title "Peer 8" -e "python3 p2p.py init 8 9 14 30" &
xterm -hold -title "Peer 9" -e "python3 p2p.py init 9 14 19 30" &
xterm -hold -title "Peer 14" -e "python3 p2p.py init 14 19 2 30" &
xterm -hold -title "Peer 19" -e "python3 p2p.py init 19 2 4 30" &