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
    DEV = False
    INSTALL_SSGUI_ONLY = False

    MAYA_API_VERSION = int(str(cmds.about(apiVersion=True))[:4])

    ANIMBUDDY_GUI_RELEASE_PATH = 'https://github.com/darkuress/animBuddy/archive/release.zip'
    ANIMBUDDY_API_RELEASE_PATH = 'https://github.com/darkuress/python-api/archive/v1.0.4.zip'

    ScriptInstallPath = {
        'Darwin': '{0}/Library/Preferences/Autodesk/maya/scripts/'.format(expanduser('~')),
        'linux64': '$HOME/maya/scripts/',
        'Windows': '{0}/maya/scripts/'.format(expanduser('~'))
    }



    PLATFORM = platform.system()
    MAYA_VERSION = cmds.about(apiVersion=True) / 10000
    IN_MAYA = False
    PYTHON_PATH = ''
    MAYA_SCRIPTS_PATH = ''
    FFMPEG_PATH = ''
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

    if MAYA_SCRIPTS_PATH not in sys.path:
        for pth in sys.path:
            if 'maya/scripts' in pth:
                MAYA_SCRIPTS_PATH = pth

    ANIMBUDDY_INSTALL_PATH = os.path.join(MAYA_SCRIPTS_PATH, 'animBuddy') 
    REQUEST_INSTALL_PATH = os.path.join(MAYA_SCRIPTS_PATH, 'requests')

    print('MAYA_SCRIPTS_PATH: {0}'.format(MAYA_SCRIPTS_PATH))
    print('PYTHON_PATH: {0}'.format(PYTHON_PATH))
    print('PIP_PATH: {0}'.format(PIP_PATH))
    print('ANIMBUDDY_INSTALL_PATH: {0}'.format(ANIMBUDDY_INSTALL_PATH))

            

    if tmpdir is None:
        tmpdir = tempfile.mkdtemp()
        delete_tmpdir = True

    # Save get-pip.py
    pipInstaller = os.path.join(tmpdir, 'get-pip.py')

    if PLATFORM == 'Darwin':
        cmd = 'curl https://bootstrap.pypa.io/get-pip.py -o {0}'.format(pipInstaller).split(' ')
        if not INSTALL_SSGUI_ONLY:
            print('Calling shell command: {0}'.format(cmd))
            print(subprocess.check_output(cmd))

    else:
        # this should be using secure https, but we shoul dbe fine for now
        # as we are only reading data, but might be a possible mid attack
        response = urllib2.urlopen('https://bootstrap.pypa.io/get-pip.py')
        data = response.read()
        with open(pipInstaller, 'w') as f:
            f.write(data)

    # Install pip
    filepath, filename = os.path.split(pipInstaller)
    sys.path.insert(0, filepath)

    if not os.path.exists(PIP_PATH):
        if PLATFORM == 'Darwin':
            cmd = '{0} {1} --user'.format('python2.7', pipInstaller).split(' ')
        else:
            cmd = '{0} {1} --user'.format(PYTHON_PATH, pipInstaller).split(' ')
        print('Calling shell command: {0}'.format(cmd))
        print(subprocess.check_output(cmd))

        # Install Dependencies
        cmd = '{0} install --force-reinstall --user {1} pyyaml requests[security]'.format(PIP_PATH,
                                                                                ANIMBUDDY_API_RELEASE_PATH).split(' ')

    # Install AnimBuddy
    if os.path.exists(ANIMBUDDY_INSTALL_PATH):
        shutil.rmtree(ANIMBUDDY_INSTALL_PATH)

    cmd = '{0} install --ignore-installed --target={1} {2}'.format(PIP_PATH, MAYA_SCRIPTS_PATH,
                                                                    ANIMBUDDY_GUI_RELEASE_PATH).split(' ')
    print('Calling shell command: {0}'.format(cmd))
    print(subprocess.check_output(cmd))

    # Install Requests
    cmd = '{0} install --ignore-installed --target={1} {2}'.format(PIP_PATH, REQUEST_INSTALL_PATH,
                                                                    'requests').split(' ')
    print('Calling shell command: {0}'.format(cmd))
    print(subprocess.check_output(cmd))

    # Remove our temporary directory
    if delete_tmpdir and tmpdir:
        print('cleaning up temporary files: {0}'.format(tmpdir))
        shutil.rmtree(tmpdir, ignore_errors=True)

    #adding to userSetup.py so that it runs when maya starts up
    userSetupFile = os.path.join(MAYA_SCRIPTS_PATH, 'userSetup.py')
    if not os.path.exists(userSetupFile):
        f= open(userSetupFile,'w+')
        f.close()

    append = True
    f = open(userSetupFile, 'r')
    for line in f:
        if 'ANIMBUDDYBOOLALA' in line:
            append = False
    f.close()

    if append:
        reqStr = REQUEST_INSTALL_PATH.replace('/', '//').replace('\\\\', '\\\\\\\\')
        f = open(userSetupFile, 'a')
        cmd = '\\n\\n#ANIMBUDDYBOOLALA\\n'
        cmd += 'import maya.cmds as cmds\\n'
        cmd += 'import sys\\n'
        cmd += 'sys.path.append(\"{}\")\\n'.format(reqStr)
        cmd += 'from animBuddy import UI\\n'
        cmd += 'reload(UI)\\n'
        cmd += 'x = UI.UI()\\n'
        cmd += 'cmds.evalDeferred(\"x.loadInMaya()\")\\n'
        f.write(cmd)
        f.close()

    sys.path.append(REQUEST_INSTALL_PATH)

    from animBuddy import UI
    reload(UI)
    x = UI.UI()
    x.loadInMaya()

