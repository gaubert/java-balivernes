#!/bin/sh

#export LD_LIBRARY_PATH=/usr/lib/oracle/xe/app/oracle/product/10.2.0/server/lib::/usr/local/lib
. /usr/lib/oracle/xe/app/oracle/product/10.2.0/server/bin/oracle_env.sh
export TNS_ADMIN=/home/aubert
CRN_HOME=/home/aubert/RNPickerEnv

logging_dir=/tmp/cronlogs
mkdir -p $logging_dir

begin_date=`date +"%m-%d-%yT%T"`
output="$logging_dir/log_output_$begin_date.log"

echo "Starting Run at $begin_date" >> $output
echo "Starting Run at $begin_date"

echo "outputs for this run are in $output"
echo "outputs for this run are in $output" >> $output

$CRN_HOME/new-env/bin/generate_products_and_email -g test >> $output 2>&1
result="$?"

end_date=`date +"%m-%d-%yT%T"`

echo "Stopping Run at $end_date. result=$result (0 success,other fail)."
echo "Stopping Run at $end_date. result=$result (0 success,other fail)." >> $output
