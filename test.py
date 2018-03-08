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

    data = payload
    data['actions'] = json_data
    saveData(data)
    print "Request: ", json_data
    print payload

    return jsonify({u'bookmark':2,u'actions':[]}), 200

def saveData(data):
    old = readData()
    print old
    old.append(data)
    writeData(old)


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
