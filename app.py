from flask import Flask, request
import zlib
import base64
import json

app = Flask(__name__)

@app.route("/v1/sync", methods=["GET", "POST"])
def sync():
    payload = json.loads(request.data)
    raw_data = base64.b64decode(payload["actions"])
    json_data = json.loads(zlib.decompress(raw_data, 16 + zlib.MAX_WBITS))

    print "Request: ", json_data

    return resp, 200

if __name__ == "__main__":
    app.run(debug=False)