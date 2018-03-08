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
    saveData(data)

    return jsonify({u'bookmark':2,u'actions':[]}), 200

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
