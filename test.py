from flask import Flask, request, jsonify
import zlib
import base64
import json

app = Flask(__name__)

@app.route("/v1/sync", methods=["GET", "POST"])
def sync():
    payload = json.loads(request.data)
    raw_data = base64.b64decode(payload["actions"])
    json_data = json.loads(zlib.decompress(raw_data, 16 + zlib.MAX_WBITS))

    data = json_data
    # saveData(data)
    mdata = [{"data": {"book_name": "test"}, "type": "add_book", "id": 0, "timestamp": 1518620066}]
    print fetchResponse(mdata)


    return jsonify({u'bookmark':2,u'actions':[]}), 200

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
        if (item not in old):
            old.append(item)

    # maybe should compare *type* value
    return sorted(old, key=lambda o:o['timestamp'])

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
    app.run(debug=False)
