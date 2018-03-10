from flask import Flask, request, jsonify
import zlib
import base64
import json
import os.path

app = Flask(__name__)

## global server action id. should init in first run
id = 0
ID_FILE_PATH = "id"
DATA_FILE_PATH = "data.json"

## deal with cli data
@app.route("/v1/sync", methods=["GET", "POST"])
def sync():
    payload = json.loads(request.data)
    raw_data = base64.b64decode(payload["actions"])
    json_data = json.loads(zlib.decompress(raw_data, 16 + zlib.MAX_WBITS))

    if json_data is None: data = []
    # extract data to response to client
    actions = fetchResponseById(payload["bookmark"])
    # save actions with generated id
    saveActionsAndGenerateId(payload["bookmark"], json_data)

    # constuct response
    response = {}
    # response["bookmark"] = lastId() # ? should I use u"bookmark" here? what is the difference?
    response[u"bookmark"] = lastId()
    response[u"actions"] = actions

    saveId()

    return jsonify(response), 200

## functions about id
def initId():
    global id
    with open(ID_FILE_PATH) as infile:
        id = json.load(infile)[u'id']

def saveId():
    with open(ID_FILE_PATH, 'w') as outfile:
        json.dump({u'id':id}, outfile)

def generateId():
    global id
    id =  id + 1
    return id

def lastId():
    return id

def saveActionsAndGenerateId(bookmark, actions):
    if bookmark == lastId():
        saveData(actions)
    elif bookmark < lastId():
        saveData(actions)
    else:
    # maybe delete all client data and re-sync?
    # but now do nothing.
        print "bookmark is greater than last id in server"

def fetchResponseById(bookmark):
    def fresh(x):
        return x["id"] > bookmark

    alldata = readData()
    actions = filter(fresh, alldata)
    return actions

def sillyDataAppend(old, data):
    for item in data:
        if (not isDuplicate(item, old)):
            item["id"] = generateId()
            old.append(item)

    # maybe should compare *type* value
    return sorted(old, key=lambda o:o['id'])

def isDuplicate(item, collections):
    for action in collections:
        if (item["timestamp"] == action["timestamp"] and item["data"] == action["data"] and item["type"] == action["type"]): return True
    return False


## functions about read/write file
def saveData(data):
    old = readData()
    newdata = sillyDataAppend(old, data)
    writeData(newdata)


def writeData(data):
    with open(DATA_FILE_PATH, 'w') as outfile:
        json.dump(data, outfile)

def readData():
    with open(DATA_FILE_PATH) as infile:
        data = json.load(infile)
        return data
    return []

## functions to initialize data files
def initDataFiles():
    if not os.path.isfile(ID_FILE_PATH):
        id = 0
        saveId()
    if not os.path.isfile(DATA_FILE_PATH):
        writeData([])

## main function
if __name__ == "__main__":
    initDataFiles()
    initId()
    app.run(debug=False)
