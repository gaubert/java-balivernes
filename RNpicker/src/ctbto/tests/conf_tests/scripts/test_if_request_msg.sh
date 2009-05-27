#!/bin/bash
#set -x

# quick script for extracting spectrum from archive file
#$1 ssh hostname (need to have a public key installed)"
#$2 dir to scan
#$3 file where to put the results
#$4 remote user
# return a the list of matching files in stdout
  

tempfile="/tmp/job.$$.remote"

cat <<EOF >> $tempfile
#!/usr/bin/perl -w
use strict;

# list directory content
my \$dir = "$2";

my @not_sorted = <\$dir/*.msg>;

my @sorted = sort { lc(\$a) cmp lc(\$b) } @not_sorted;
  
my \$arrsize = @sorted;

if (\$arrsize <=0)
{
   printf "No sql files found into %s\n",\$dir;
   exit 1;
}

my \$fhandle;
my \$find = "REQUEST";
my \$find_data = "MSG_TYPE\\\s+DATA";

my \$ok = -1;

foreach my \$file (@sorted)
{
  open(\$fhandle,"<\$file") or die "Warning. Cannot not open remote file \$file on machine \$1. Error code: \$! \n";
  while (<\$fhandle>)
  {
    my \$line = \$_;
    if (\$line =~ m/\$find/i)
    {
       \$ok = 0;
    }
    
    if (\$line =~ m/\$find_data/i)
    {
       #quit as we only want request
       \$ok = -1;
       last;
    }
  }
  
   if (\$ok == 0)
   {
     print "\$file\n";
     \$ok = -1;
   }
   else
   {
     \$ok = -1;
   }
  
  #close($fhandle);
}

exit 0;
EOF

cat $tempfile | ssh $4@$1 perl > $3
#cat $tempfile | ssh $4@$1 perl 
res="$?"

rm -f $tempfile

if [ $res != 0 ];
then
  echo "Error.delete $3"
  #rm -f $3
fi


exit $res


