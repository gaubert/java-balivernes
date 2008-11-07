#!/bin/bash

# $1 is the src (what to get)
# $2 is where to put it
# $3 Host where to connect

# create temporary filename
TFILE="/tmp/$(basename $0).$$.tmp"

#echo "cd /home/misc/rmsops/data/spectrum/$1/" >> $TFILE
echo "get $1 $2" >> $TFILE

sftp -b $TFILE aubert@$3
res=$?

rm -f $TFILE

exit $res
