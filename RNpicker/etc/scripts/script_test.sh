#!/bin/sh

#set -x

# Runs on Linux
#################################
## RNPicker Distribution home directory
#################################
RNPICKER_HOME=.

#################################
## if RNPICKER_HOME is relative,
## build the absolute path
#################################
D=`dirname "$RNPICKER_HOME"`
B=`basename "$RNPICKER_HOME"`
RNPICKER_HOME="`cd \"$D\" 2>/dev/null && pwd || echo \"$D\"`/$B"

#################################
## RNPicker necessary information
#################################
PYTHON_BIN=$RNPICKER_HOME/bin
LIBXML2=
LIBXSLT=
ORACLE_HOME=

#################################
## You probably do not want to
## change anything from there
#################################

echo "RNPICKER_HOME distribution directory $RNPICKER_HOME"





###################################
## create bootstrap and launch program
## the bootstrap is always under 
## /tmp/rnpicker.bootstrap
###################################


# keep args in variables
ARGS="$@"

cat > /tmp/rnpicker.bootstrap << EOF
import ctbto.run.generate_arr as runner
runner.run()
EOF

#./generate_arr $ARGS
$PYTHON_HOME/bin/python /tmp/rnpicker.bootstrap $ARGS



