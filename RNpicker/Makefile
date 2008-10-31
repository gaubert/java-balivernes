#=============================================================================
# File: Simple Makefile for RNPicker project
# author: guillaume.aubert@ctbto.org
#=============================================================================
BASEDIR=.
DIST=$(BASEDIR)/dist
BUILDDIST=$(BASEDIR)/build/dist
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

clean:
	cd $(DIST); rm -Rf build; rm -Rf RNPicker.egg-info; rm -Rf dist

    


