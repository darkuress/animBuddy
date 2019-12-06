import requests
import os
from animBuddy.Utils import System
reload(System)

class License(object):
    """
    """
    def __init__(self, key):
        """
        """
        self.key = key

    def validate(self):
        """
        """
        response = requests.get("http://animbuddy.pythonanywhere.com/license/{}".format(self.key))
        result = response.json()['result']
        return result

    @staticmethod
    def readLicense():
        """
        """
        licenseFile = os.path.join(System.dataPath(), 'license')
        if not os.path.exists(licenseFile):
            return False
        else:
            f = open(licenseFile, "r")
            key = str(f.read())
            f.close()
            return key

    @staticmethod
    def writeLicense(key):
        """
        """
        licenseFile = os.path.join(System.dataPath(), 'license')
        if os.path.exists(licenseFile):
            os.remove(licenseFile)
        f = open(licenseFile, "w")
        f.write(key)
        f.close()
        return True