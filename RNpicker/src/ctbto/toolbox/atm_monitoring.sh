#!/bin/sh
#set -x

# Python distribution. Note that a Python 2.5 or more is needed
PYTHON_HOME=/home/smd/aubert/public/generate_and_email_runtime

#ECACCESS_HOME distribution
export ECACCESS_HOME=/home/smd/aubert/public/atm_monitoring/ecaccess-v3.3.0

# list of people that will receive emails in case of problems
export ATM_MON_RECEIVERS='guillaume.aubert@ctbto.org,guillaume.aubert@gmail.com'

#run script
$PYTHON_HOME/bin/python ./monitor_atm_transfers.py

res=$?

exit $res
