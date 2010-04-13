#!/bin/sh

# Python distribution. Note that a Python 2.5 or more is needed
PYTHON_HOME=/home/smd/aubert/public/generate_and_email_runtime

ATM_MON_HOME=/home/smd/aubert/public/atm_monitoring/monitoring-cron

#ECACCESS_HOME distribution
export ECACCESS_HOME=/home/smd/aubert/public/atm_monitoring/ecaccess-v3.3.0


# list of people that will receive emails in case of problems
export ATM_MON_RECEIVERS='guillaume.aubert@ctbto.org,guillaume.aubert@gmail.com'
#export ATM_MON_RECEIVERS=$1

#name of the gateway that is been checked
export GATEWAY_NAME='CTBTO4'

echo "********** check $GATEWAY_NAME **********"

export ECCERTFILE=/home/smd/aubert/public/atm_monitoring/certs/cba/.eccert.crt
#run script
$PYTHON_HOME/bin/python $ATM_MON_HOME/monitor_atm_transfers.py
ctbto4_result=$?

echo "********** $GATEWAY_NAME checking done **********"

#name of the gateway that is been checked
export GATEWAY_NAME='WIRNAPPS'

echo "********** check $GATEWAY_NAME **********"

export ECCERTFILE=/home/smd/aubert/public/atm_monitoring/certs/cbb/.eccert.crt
#run script
$PYTHON_HOME/bin/python $ATM_MON_HOME/monitor_atm_transfers.py
wirnapps_result=$?

echo "********** $GATEWAY_NAME checking done **********"

if [ $ctbto4_result -gt 0 ] || [ $wirnapps_result -gt 0 ] ; then
 exit 1
else
 exit 0
fi
