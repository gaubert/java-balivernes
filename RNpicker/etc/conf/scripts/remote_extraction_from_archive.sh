#!/bin/bash
#set -x

# quick script for extracting spectrum from archive file
#$1 ssh hostname (need to have a public key installed)"
#$2 file to access
#$3 offset to reach
#$4 size to read
#$5 local file where to put the results
#$6 remote user
# return a spectrum in stdout


tempfile="/tmp/job.$$.remote"

cat <<EOF >> $tempfile
#!/usr/bin/perl -w

my \$DEFAULT_BLOCKSIZE= 1024;

my \$fhandle;
my \$pos = $3;

# read 1KB
my \$blocksize = \$DEFAULT_BLOCKSIZE;
my \$n;
my \$total = $4;

open(\$fhandle,"<$2") or die "Couldn't open remote file $2 on machine $1. Error code: \$! \n";

seek(\$fhandle, \$pos, 0)     or die "Couldn't seek to \$pos. Error code: \$!\n";

while ( (\$total > 0) && ( (\$n = read(\$fhandle,\$buffer,\$blocksize)) > 0 ) )
{
   # print buffer
   print "\$buffer";

   \$total = \$total - \$n;

   # resize buffer to read when left to read become inferior to buffer size
   \$blocksize = \$total if (\$total < \$blocksize);
}
exit 0;
EOF

cat $tempfile | ssh $6@$1 perl > $5
res="$?"

rm -f $tempfile

if [ $res != 0 ];
then
  echo "Error.delete $5"
  rm -f $5
fi


exit $res


