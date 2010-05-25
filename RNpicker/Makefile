#=============================================================================
# File: Simple Makefile for RNPicker project
# author: guillaume.aubert@ctbto.org
#=============================================================================
BASEDIR=.
# internal dirs
DISTS=$(BASEDIR)/dists

#RNDist info
RNDIST=$(DISTS)/rnpicker-ppath-dist
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
PYTHONVERSION=2.5

# new version 1.2.4 released 310709
# new version 1.3.0 released 010210
# new version 1.3.1 released 050310
# new version 1.3.2 released 160310
# new version 1.3.3.1 released 270410 
# new version 1.3.3.2 released 270410 

RNVERSION=1.3.4
RNDISTNAME=rnpicker-$(RNVERSION)

CONFVERSION=0.8
CONFDISTNAME=conf-$(CONFVERSION)


#all: rn-src-dist conf-src-dist

all: rn-ppath-dist

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

rn-ppath-dist: clean init conf-src-egg-dist 
	# need to copy sources in distributions as distutils does not always support symbolic links (pity)
	mkdir -p $(RNDIST)/RNPicker-$(RNVERSION)
	#add rnpicker sources
	mkdir -p $(RNDIST)/RNPicker-$(RNVERSION)/lib/ctbto
	cp -R $(BASEDIR)/src/ctbto $(RNDIST)/RNPicker-$(RNVERSION)/lib
	# copy shell scripts in dist/bin
	mkdir -p $(RNDIST)/RNPicker-$(RNVERSION)/bin
	cp -R $(BASEDIR)/etc/scripts/generate_NG_arr_with_python_path $(RNDIST)/RNPicker-$(RNVERSION)/bin/generate_NG_arr
	cp -R $(BASEDIR)/etc/scripts/generate_products_and_email $(RNDIST)/RNPicker-$(RNVERSION)/bin/generate_products_and_email
	# copy conf files
	cp -R $(BASEDIR)/etc/conf $(RNDIST)/RNPicker-$(RNVERSION)
	#add dependency: conf-egg-dist 
	#cp $(CONFDIST)/build/conf-1.1-py$(PYTHONVERSION).egg $(RNDIST)/RNPicker-$(RNVERSION)/lib
	#cd $(RNDIST); tar zcvf ./RNPicker-$(RNVERSION).tar.gz ./RNPicker-$(RNVERSION)
	#echo "distribution stored in $(RNDIST)"
	#add dependency: conf-src-egg-dist 
	cp -R $(CONFBUILDDIST)/org $(RNDIST)/RNPicker-$(RNVERSION)/lib
	cd $(RNDIST); tar zcvf ./RNPicker-$(RNVERSION).tar.gz ./RNPicker-$(RNVERSION)
	echo "distribution stored in $(RNDIST)"

conf-src-dist: clean init 
	# need to copy sources in distributions as distutils does not always support symbolic links (pity)
	cp -R $(BASEDIR)/conf-src/org $(CONFDIST)
	cd $(CONFDIST); $(PYTHONBIN) setup.py sdist -d ../../$(CONFBUILD) 
	echo "distribution stored in $(CONFBUILD)"

conf-src-egg-dist: init
	# need to copy sources in distributions as distutils does not always support symbolic links (pity)
	mkdir -p $(CONFBUILDDIST)
	cp -R $(BASEDIR)/conf-src/org $(CONFBUILDDIST)
	echo "distribution stored in $(CONFBUILDDIST)"

conf-egg-dist: init 
	cp -R $(BASEDIR)/conf-src/org $(CONFDIST)
	cd $(CONFDIST); $(PYTHONBIN) setup.py bdist_egg -b /tmp/build -p $(CONFDISTNAME) -d ../../$(CONFBUILDDIST) 
	echo "distribution stored in $(CONFBUILDDIST)"

clean: clean-build
	cd $(RNDIST); rm -Rf build; rm -Rf RNPicker.egg-info; rm -Rf ctbto; rm -Rf conf; rm -Rf scripts
	cd $(CONFDIST); rm -Rf build; rm -Rf conf.egg-info; rm -Rf dist; rm -Rf org
	
clean-build:
	cd $(RNBUILD); rm -Rf egg-dist; 
	rm -Rf $(RNDIST)/RNPicker-*
	cd $(CONFBUILD); rm -Rf egg-dist

    


