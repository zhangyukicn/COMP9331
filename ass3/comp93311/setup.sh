#!/usr/bin/env bash
# Authored by Rui.Mu
# Wechat:marey_marey111
#
#
# How to use?
#
# For Mac OS X uers only. Linux user may install xterm and use the script provided by the lecturer.
# Windows users, well, have a nice day.
#
# Paste this file to your working directory.
# Use Terminal or iTerm to go to your working directory.
#
# First step:
# run
#   $ chmod +x ./setup.sh
# to make it executable
#
# Second step:
# run
#   $ ./setup.sh
#
# You are free to improve this script, enjoy.


current_path= "$PWD"
osascript - "$@" <<EOF
tell application "Terminal"
    activate
    set shell1 to do script "cd ${PWD}"
    delay 1
    do script "echo 'Youtube上关注登登教育，更多资料请加微信:marey_marey111'" in shell1
    do script "python3 p2p.py init 2 4 5 30" in shell1
    set custom title of shell1 to "Peer 2"

    set shell2 to do script "cd ${PWD}"
    delay 1
    do script "echo 'Youtube上关注登登教育，更多资料请加微信:marey_marey111'" in shell2
    do script "python3 p2p.py init 4 5 8 30" in shell2
    set custom title of shell2 to "Peer 4"

    set shell3 to do script "cd ${PWD}"
    delay 1
    do script "echo 'Youtube上关注登登教育，更多资料请加微信:marey_marey111'" in shell3
    do script "python3 p2p.py init 5 8 9 30" in shell3
    set custom title of shell3 to "Peer 5"

    set shell4 to do script "cd ${PWD}"
    delay 1
    do script "echo 'Youtube上关注登登教育，更多资料请加微信:marey_marey111'" in shell4
    do script "python3 p2p.py init 8 9 14 30" in shell4
    set custom title of shell4 to "Peer 8"

    set shell5 to do script "cd ${PWD}"
    delay 1
    do script "echo 'Youtube上关注登登教育，更多资料请加微信:marey_marey111'" in shell5
    do script "python3 p2p.py init 9 14 19 30" in shell5
    set custom title of shell5 to "Peer 9"

    set shell6 to do script "cd ${PWD}"
    delay 1
    do script "echo 'Youtube上关注登登教育，更多资料请加微信:marey_marey111'" in shell6
    do script "python3 p2p.py init 14 19 2 30" in shell6
    set custom title of shell6 to "Peer 14"

    set shell7 to do script "cd ${PWD}"
    delay 1
    do script "echo 'Youtube上关注登登教育，更多资料请加微信:marey_marey111'" in shell7
    do script "python3 p2p.py init 19 2 4 30" in shell7
    set custom title of shell7 to "Peer 19"

end tell
EOF
