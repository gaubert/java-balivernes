#!/bin/bash

# $1 is the src (what to get)
# $2 is where to put it

# create temporary filename
TFILE="/tmp/$(basename $0).$$.tmp"

#echo "cd /home/misc/rmsops/data/spectrum/$1/" >> $TFILE
echo "get $1 $2" >> $TFILE

sftp -b $TFILE aubert@kuredu
res=$?

rm -f $TFILE

exit $res
