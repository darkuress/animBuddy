import os

def dataPath():
    filePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    dataPath = os.path.join(filePath, 'animBuddyData')
    if not os.path.exists(dataPath):
        os.mkdir(dataPath)
    return dataPath
