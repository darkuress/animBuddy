import os
import urllib2
import sys

import logging
logger = logging.getLogger("AnimBuddy")

def getLatestSetupPyFileFromRepo():
    """Parses latest setup.py's version number"""
    response = urllib2.urlopen(
        'https://raw.githubusercontent.com/darkuress/animBuddy/release/setup.py')
    html = response.read()
    return html.split("version = '")[1].split("',")[0]

def getLatestSetupPyFileFromLocal():
    """Checks locally installed packages version number"""
    filePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    setupFile = os.path.join(filePath, "setup.py")
    f = open(setupFile, "r")
    return f.read().split("version = '")[1].split("',")[0]

def getVersionDifference():
    """Returns the difference between local Package and latest Remote"""
    remote = int(getLatestSetupPyFileFromRepo().replace(".", ""))
    local = int(getLatestSetupPyFileFromLocal().replace(".", ""))
    if remote > local:
        logger.info("Local Version : {} Remote Version {}".format(remote, local))
        return remote-local
    else:
        return False