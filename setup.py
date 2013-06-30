
from distutils.core import setup  
import sys, py2exe, os
 
options = {
	"py2exe": {
		"compressed": 1,  
        "optimize": 2,
        "includes": ["urllib2", "optparse", "bs4", "serial", "time"],  
        "bundle_files": 1,
		"dll_excludes": ["msvcr71.dll"],
    }
}

setup(
    version = "0.3.0",  
    description = "mytest",  
    name = "mytest",  
    options = options,  
    zipfile = None,
    console = [{"script": "mytest.py"}],
) 
