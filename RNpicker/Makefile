#=============================================================================
# File: Simple Makefile for RNPicker project
# author: guillaume.aubert@ctbto.org
#=============================================================================
BASEDIR=.
# internal dirs
DIST=$(BASEDIR)/dist
BUILD=$(BASEDIR)/build
BUILDDIST=$(BUILD)/egg-dist
ETC=$(BASEDIR)/etc

PYTHONBIN=/usr/bin/python

VERSION=0.5
DISTNAME=rnpicker-$(VERSION)


all: egg-dist

init:
	mkdir -p $(DIST)
	mkdir -p $(BUILDDIST)

egg-dist: init 
	cd $(DIST); $(PYTHONBIN) setup.py bdist_egg -b /tmp/build -p $(DISTNAME) -d ../$(BUILDDIST) 

clean: clean-build
	cd $(DIST); rm -Rf build; rm -Rf RNPicker.egg-info
	
clean-build:
	cd $(BUILD); rm -Rf egg-dist

    


