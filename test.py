from flask import Flask, request, jsonify
import zlib
import base64
import json

app = Flask(__name__)

## global server action id. should init in first run
id = 0

@app.route("/v1/sync", methods=["GET", "POST"])
def sync():
    payload = json.loads(request.data)
    raw_data = base64.b64decode(payload["actions"])
    json_data = json.loads(zlib.decompress(raw_data, 16 + zlib.MAX_WBITS))

    data = json_data
    if data is None: data = []
    # saveData(data)
    # mdata = [{"data": {"book_name": "test"}, "type": "add_book", "id": 0, "timestamp": 1518620066}]
    # print fetchResponse(mdata)
    # extract data to response to client
    actions = fetchResponseById(payload["bookmark"])
    # save actions with generated id
    saveActionsAndGenerateId(payload["bookmark"], data)
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
    with open('./id') as infile:
        id = json.load(infile)[u'id']

def saveId():
    with open('./id', 'w') as outfile:
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


## function about timestamp
def fetchResponse(data):
    def fresh(x):
        return x["timestamp"] > maxTimestamp

    maxTimestamp = getMaxTs(data)
    print maxTimestamp
    alldata = readData()
    actions = filter(fresh, alldata)
    return actions

def getMaxTs(data):
    return sorted(data, key=lambda o:o['timestamp'])[-1]["timestamp"]

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


def saveData(data):
    old = readData()
    newdata = sillyDataAppend(old, data)
    writeData(newdata)


def writeData(data):
    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)

def readData():
    with open("data.json") as infile:
        data = json.load(infile)
        return data
    return []

if __name__ == "__main__":
    initId()
    app.run(debug=False)
