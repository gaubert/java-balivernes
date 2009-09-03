#!/bin/bash

export INFRAPROFILER_CONF_DIR=/home/smd/aubert/public/infrasound/profile-test-env/conf

export G2SPATH=/home/smd/aubert/public/infrasound/g2s_profile_generator

export LD_LIBRARY_PATH=/home/smd/aubert/public/infrasound/g2s_profile_generator/lib

/home/smd/aubert/public/infrasound/infrasound_profile_runtime/bin/python run_g2s_and_create_netcdf.py
