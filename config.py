import json

def getProperty(property):
    myfile = open('config.json', 'r')
    jsondata = myfile.read()
    obj = json.loads(jsondata)
    return obj["{}".format(property)]

