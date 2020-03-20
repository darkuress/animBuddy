import os
import sys
import shutil
from maya import cmds
from datetime import datetime, timedelta
import glob
import urllib2
import tempfile
import subprocess
import platform
from os.path import expanduser
import zipfile
import maya.cmds as cmds
from functools import partial

def run():
    INSTALL_SSGUI_ONLY = False

    MAYA_API_VERSION = int(str(cmds.about(apiVersion=True))[:4])

    ANIMBUDDY_API_RELEASE_PATH = 'https://github.com/darkuress/animBuddy/archive/release.zip'

    ScriptInstallPath = {
        'Darwin': '{0}/Library/Preferences/Autodesk/maya/scripts/'.format(expanduser('~')),
        'linux64': '$HOME/maya/scripts/',
        'Windows': '{0}/maya/scripts/'.format(expanduser('~'))
    }

    PLATFORM = platform.system()
    MAYA_VERSION = cmds.about(apiVersion=True) / 10000
    PYTHON_PATH = ''
    MAYA_SCRIPTS_PATH = ''
    PIP_PATH = ''
    tmpdir = None
    delete_tmpdir = False
    cmd = ''

    if PLATFORM == 'Windows':
        PYTHON_PATH = os.path.join(os.getenv('MAYA_LOCATION'), 'bin', 'mayapy.exe')
        MAYA_SCRIPTS_PATH = ScriptInstallPath['Windows']
        PIP_PATH = os.path.join(os.getenv('APPDATA'), 'Python', 'Scripts', 'pip2.7.exe')

    elif PLATFORM == 'Darwin':
        PYTHON_PATH = '/usr/bin/python'
        MAYA_SCRIPTS_PATH = ScriptInstallPath['Darwin']
        PIP_PATH = os.path.join(expanduser('~'), 'Library', 'Python', '2.7', 'bin', 'pip2.7')

    if MAYA_SCRIPTS_PATH not in sys.path and MAYA_SCRIPTS_PATH[:-1] not in sys.path:
        for pth in sys.path:
            if 'maya/scripts' in pth:
                MAYA_SCRIPTS_PATH = pth

    ANIMBUDDY_INSTALL_PATH = os.path.join(MAYA_SCRIPTS_PATH, 'animBuddy') 
    REQUEST_INSTALL_PATH = os.path.join(MAYA_SCRIPTS_PATH, 'requests')

    print('MAYA_SCRIPTS_PATH: {0}'.format(MAYA_SCRIPTS_PATH))
    print('PYTHON_PATH: {0}'.format(PYTHON_PATH))
    print('PIP_PATH: {0}'.format(PIP_PATH))
    print('ANIMBUDDY_INSTALL_PATH: {0}'.format(ANIMBUDDY_INSTALL_PATH))

    # delete AnimBuddy
    if os.path.exists(ANIMBUDDY_INSTALL_PATH):
        shutil.rmtree(ANIMBUDDY_INSTALL_PATH)

    # delete Request
    if os.path.exists(REQUEST_INSTALL_PATH):
        shutil.rmtree(REQUEST_INSTALL_PATH)

    #delete animBuddy-x.x.x.dist-info
    ppath = os.path.dirname(ANIMBUDDY_INSTALL_PATH)
    for fldr in os.listdir(ppath):
        if fldr.startswith('animBuddy') and fldr.endswith('dist-info'):
            shutil.rmtree(os.path.join(ppath, fldr))

    #adding to userSetup.py so that it runs when maya starts up
    userSetupFile = os.path.join(MAYA_SCRIPTS_PATH, 'userSetup.py')
    delete_list = ["#ANIMBUDDYBOOLALA", "requests", "fron animBuddy", "reload(UI)", "x = UI.UI()", "x.loadInMaya()"] 
    f = open(userSetupFile, 'r')
    lst = []
    for line in f:
        delete_line = False
        for word in delete_list:
            if word in line:
                delete_line = True
        if not delete_line:
            lst.append(line)
    f.close()
    f = open(userSetupFile,'w')
    for line in lst:
        f.write(line)
    f.close()