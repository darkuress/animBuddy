import requests

class Connection(object):
    """
    """
    @staticmethod
    def connect(method, key):
        """
        """
        response = requests.get("http://animbuddy.pythonanywhere.com/{}/{}".format(method, key))
        result = response.json()['result']
        return result

    @staticmethod
    def getLicense(method, user, email):
        """
        """
        response = requests.get("http://animbuddy.pythonanywhere.com/{}/{}/{}".format(method, user, email))
        result = response.json()['result']
        return result    
