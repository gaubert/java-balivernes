#!/bin/sh
#set -x

# Runs on Linux
#################################
## RNPicker Distribution home directory
#################################
RNPICKER_HOME=..

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
PYTHON_BIN=$RNPICKER_HOME/bin/python

# /usr/lib/oracle/xe/app/oracle/product/10.2.0/server
DEFAULT_ORACLE_HOME=/usr/lib/oracle/xe/app/oracle/product/10.2.0/server

DEFAULT_LIBXML2_DIR=/usr/lib

DEFAULT_LIBXSLT_DIR=/usr/lib

#################################
## You probably do not want to
## change anything from there
#################################

##################################
## Apply Default Settings if global not defined
##################################
if [ -z "$ORACLE_HOME" ]; then
   echo "ORACLE_HOME is undefined. Set it to default=($DEFAULT_ORACLE_HOME)"
   ORACLE_HOME=$DEFAULT_ORACLE_HOME
fi

if [ -z "$LIBXML2_DIR" ]; then
   echo "LIBXML2_DIR is undefined. Set it to default=($DEFAULT_LIBXML2_DIR)"
   LIBXML2_DIR=$DEFAULT_LIBXML2_DIR
fi

if [ -z "$LIBXSLT_DIR" ]; then
   echo "LIBXSLT_DIR is undefined. Set it to default=($DEFAULT_LIBXSLT_DIR)"
   LIBXSLT_DIR=$DEFAULT_LIBXSLT_DIR
fi

####################################
## Checkings
####################################

if [ ! -f "$ORACLE_HOME/lib/libclntsh.so" ]; then
    echo "ORACLE_HOME: [$ORACLE_HOME] is not an oracle distribution"
    echo "Please set the ORACLE_HOME variable globally or set DEFAULT_ORACLE_HOME (defined in this script) to an oracle distribution"
    exit 1
else
    export ORACLE_HOME
fi

if [ ! -f "$LIBXML2_DIR/libxml2.so" ]; then
    echo "LIBXML2_DIR: [$LIBXML2_DIR] doesn\'t contain libxml2.so"
    echo "Please set the LIBXML2_DIR variable globally or set DEFAULT_LIBXML2_DIR (defined in this script) to a directory containing libxml2.so"
    exit 1
else
    LD_LIBRARY_PATH=$LIBXML2_DIR:$LD_LIBRARY_PATH 
fi

if [ ! -f "$LIBXSLT_DIR/libxslt.so" -a ! -f "$LIBXSLT_DIR/lib/libexslt.so" ]; then
    echo "LIBXSLT_DIR: [$LIBXSLT_DIR] doesn\'t contain libexslt.so"
    echo "Please set the LIBXSLT_DIR variable globally or set DEFAULT_LIBXSLT_DIR (defined in this script) to a directory containing libxslt.so and libexslt.so"
    exit 1
else
    LD_LIBRARY_PATH=$LIBXSLT_DIR:$LD_LIBRARY_PATH 
fi

export LD_LIBRARY_PATH


echo "LD_LIBRARY_PATH $LD_LIBRARY_PATH"
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
$PYTHON_BIN /tmp/rnpicker.bootstrap $ARGS



