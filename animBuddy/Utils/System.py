import os
import sys
import platform

class SystemPath:
    ScriptInstallPath = {
        'Darwin': '{0}/Library/Preferences/Autodesk/maya/scripts/'.format(os.path.expanduser('~')),
        'linux64': '$HOME/maya/scripts/',
        'Windows': '{0}/maya/scripts/'.format(os.path.expanduser('~'))
    }
    PLATFORM = platform.system()
    if PLATFORM == 'Windows':
        PYTHON_PATH = os.path.join(os.getenv('MAYA_LOCATION'), 'bin', 'mayapy.exe')
        MAYA_SCRIPTS_PATH = ScriptInstallPath['Windows']
        PIP_PATH = os.path.join(os.getenv('APPDATA'), 'Python', 'Scripts', 'pip2.7.exe')

    elif PLATFORM == 'Darwin':
        PYTHON_PATH = '/usr/bin/python'
        MAYA_SCRIPTS_PATH = ScriptInstallPath['Darwin']
        PIP_PATH = os.path.join(os.path.expanduser('~'), 'Library', 'Python', '2.7', 'bin', 'pip2.7')

    if MAYA_SCRIPTS_PATH not in sys.path and MAYA_SCRIPTS_PATH[:-1] not in sys.path:
        for pth in sys.path:
            if 'maya/scripts' in pth:
                print(pth)
                MAYA_SCRIPTS_PATH = pth

    ANIMBUDDY_INSTALL_PATH = os.path.join(MAYA_SCRIPTS_PATH, 'animBuddy') 
    REQUEST_INSTALL_PATH = os.path.join(MAYA_SCRIPTS_PATH, 'requests')

def apiPath():
    """
    """
    return SystemPath.ANIMBUDDY_INSTALL_PATH

def requestsPath():
    """
    """
    return SystemPath.REQUEST_INSTALL_PATH

def dataPath():
    """
    return anim buddy data path
    """
    filePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    dataPath = os.path.join(filePath, 'animBuddyData')
    if not os.path.exists(dataPath):
        os.mkdir(dataPath)
    return dataPath

