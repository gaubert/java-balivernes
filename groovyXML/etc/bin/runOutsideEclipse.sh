#!/bin/bash

/home/aubert/dev/groovy/groovy-1.5.4/bin/groovy -Dconfig.path=/home/aubert/ecmwf/workspace/groovyXML/conf/xmlsucker.config -cp ../libs/ojdbc14_g.jar:../libs/ojdbc14dms_g.jar:../libs/orai18n.jar ./common/xmlsucker.groovy
