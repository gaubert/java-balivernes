#=============================================================================
# File: Simple Makefile for RNPicker project
# author: guillaume.aubert@ctbto.org
#=============================================================================
BASEDIR=.
# internal dirs
DISTS=$(BASEDIR)/dists

#RNDist info
RNDIST=$(DISTS)/rnpicker-dist
RNBUILD=$(RNDIST)/build
RNBUILDDIST=$(RNDIST)/build/egg-dist

#ConfDist info
CONFDIST=$(DISTS)/conf-dist
CONFBUILD=$(CONFDIST)/build
CONFBUILDDIST=$(CONFDIST)/build/egg-dist

BUILD=$(BASEDIR)/build
BUILDDIST=$(BUILD)/egg-dist
ETC=$(BASEDIR)/etc

PYTHONBIN=/usr/bin/python

RNVERSION=0.5
RNDISTNAME=rnpicker-$(RNVERSION)

CONFVERSION=0.8
CONFDISTNAME=conf-$(VERSION)


all: conf-egg-dist

init:
	mkdir -p $(RNDIST)
	mkdir -p $(RNBUILDDIST)
	mkdir -p $(CONFDIST)
	mkdir -p $(CONFBUILDDIST)

rn-egg-dist: init 
	cd $(RNDIST); $(PYTHONBIN) setup.py bdist_egg -b /tmp/build -p $(RNDISTNAME) -d ../../$(RNBUILDDIST) 
	echo "distribution stored in $(RNBUILDDIST)"

conf-egg-dist: init 
	cd $(CONFDIST); $(PYTHONBIN) setup.py bdist_egg -b /tmp/build -p $(CONFDISTNAME) -d ../../$(CONFBUILDDIST) 
	echo "distribution stored in $(CONFBUILDDIST)"

clean: clean-build
	cd $(RNDIST); rm -Rf build; rm -Rf RNPicker.egg-info
	cd $(CONFDIST); rm -Rf build; rm -Rf RNPicker.egg-info
	
clean-build:
	cd $(RNBUILD); rm -Rf egg-dist
	cd $(CONFBUILD); rm -Rf egg-dist

    


