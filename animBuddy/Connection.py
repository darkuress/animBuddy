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
