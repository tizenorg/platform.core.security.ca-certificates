#!/bin/bash

SRC_PATH=$1
CRT_PATH=$2

if [ -s $CRT_PATH ]
then
    rm $CRT_PATH
fi

for i in `find $SRC_PATH -maxdepth 1 -type f`
do
    openssl x509 -in $i -outform PEM >> $CRT_PATH 
done

