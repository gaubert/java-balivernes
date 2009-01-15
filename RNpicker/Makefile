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
CONFBUILDDIST=$(CONFDIST)/build

BUILD=$(BASEDIR)/build
BUILDDIST=$(BUILD)/egg-dist
ETC=$(BASEDIR)/etc

PYTHONBIN=/usr/bin/python

RNVERSION=0.5
RNDISTNAME=rnpicker-$(RNVERSION)

CONFVERSION=0.8
CONFDISTNAME=conf-$(CONFVERSION)


all: rn-src-dist

init:
	mkdir -p $(RNDIST)
	mkdir -p $(RNBUILDDIST)
	mkdir -p $(CONFDIST)
	mkdir -p $(CONFBUILDDIST)

rn-egg-dist: init 
	cp -R $(BASEDIR)/src/ctbto $(RNDIST)
	cd $(RNDIST); $(PYTHONBIN) setup.py bdist_egg -b /tmp/build -p $(RNDISTNAME) -d ../../$(RNBUILDDIST) 
	echo "distribution stored in $(RNBUILDDIST)"

rn-src-dist: clean init 
	# need to copy sources in distributions as distutils does not always support symbolic links (pity)
	cp -R $(BASEDIR)/src/ctbto $(RNDIST)
	# copy scripts in dist
	cp -R $(BASEDIR)/etc/scripts $(RNDIST)
	cp -R $(BASEDIR)/etc/conf $(RNDIST)
	cd $(RNDIST); $(PYTHONBIN) setup.py sdist -d ../../$(RNBUILD) 
	echo "distribution stored in $(RNBUILD)"

conf-src-dist: clean init 
	# need to copy sources in distributions as distutils does not always support symbolic links (pity)
	cp -R $(BASEDIR)/conf-src/org $(CONFDIST)
	cd $(CONFDIST); $(PYTHONBIN) setup.py sdist -d ../../$(CONFBUILD) 
	echo "distribution stored in $(CONFBUILD)"

conf-egg-dist: init 
	cp -R $(BASEDIR)/conf-src/org $(CONFDIST)
	cd $(CONFDIST); $(PYTHONBIN) setup.py bdist_egg -b /tmp/build -p $(CONFDISTNAME) -d ../../$(CONFBUILDDIST) 
	echo "distribution stored in $(CONFBUILDDIST)"

clean: clean-build
	cd $(RNDIST); rm -Rf build; rm -Rf RNPicker.egg-info
	cd $(CONFDIST); rm -Rf build; rm -Rf conf.egg-info; rm -Rf dist
	
clean-build:
	cd $(RNBUILD); rm -Rf egg-dist
	cd $(CONFBUILD); rm -Rf egg-dist

    


