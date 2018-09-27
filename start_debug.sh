#!/bin/bash
#pid=$(adb jdwp |tail -n 1)
pname=$1
#pid=$(adb shell ps |grep $pname |awk '{print $1}')
adb shell am set-debug-app -w $pname
pid=$(adb shell ps |grep $pname |grep -v ":\|/" |head -n 1 |awk '{print $2}' )
echo $pid
adb forward tcp:7777 jdwp:$pid
rlwrap jdb -sourcepath ./smali/ -attach localhost:7777
