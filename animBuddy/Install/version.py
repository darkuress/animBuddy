import os
import urllib2
import sys

import logging
logger = logging.getLogger("AnimBuddy")

#This is Local Version
VERSION = "1.0.2"

def getLatestSetupPyFileFromRepo():
    """Parses latest setup.py's version number"""
    response = urllib2.urlopen(
        'https://raw.githubusercontent.com/darkuress/animBuddy/release/setup.py')
    html = response.read()
    return html.split("version = '")[1].split("',")[0]

def getLatestSetupPyFileFromLocal():
    return VERSION

def getVersionDifference():
    """Returns the difference between local Package and latest Remote"""
    remote = int(getLatestSetupPyFileFromRepo().replace(".", ""))
    local = int(getLatestSetupPyFileFromLocal().replace(".", ""))
    if remote > local:
        logger.info("Local Version : {} Remote Version {}".format(remote, local))
        return remote-local
    else:
        return False