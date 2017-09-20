#!/bin/bash 
echo $@
grep sshd $1
danger=`grep sshd $1 | grep -i "fail"`
if [ -n $danger ]; then
    echo NOTIFICATION_COLOR=RED
fi
