from flask import Flask, jsonify, send_from_directory, request
import os
import json
from datetime import datetime

# Store latest device status (in-memory)
latest_status = {
    "device_id": "ESP32_01",
    "firmware": "unknown",
    "state": "unknown",
    "message": "no data yet",
    "timestamp": None
}


app = Flask(__name__)

# --------------------------------------------------
# Resolve absolute paths (works locally + on Render)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

METADATA_PATH = os.path.join(BASE_DIR, "metadata.json")
FIRMWARE_FOLDER = os.path.join(BASE_DIR, "..", "firmware")


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/metadata", methods=["GET"])
def metadata():
    try:
        with open(METADATA_PATH, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "error": "Failed to load metadata",
            "details": str(e)
        }), 500


@app.route("/firmware/<path:filename>", methods=["GET"])
def firmware(filename):
    try:
        return send_from_directory(FIRMWARE_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return jsonify({
            "error": "Failed to send firmware",
            "details": str(e)
        }), 500

@app.route('/status', methods=['POST'])
def receive_status():
    global latest_status
    data = request.get_json(force=True)

    latest_status = {
        "device_id": data.get("device_id", "ESP32_01"),
        "firmware": data.get("firmware"),
        "state": data.get("state"),
        "message": data.get("message"),
        "timestamp": datetime.utcnow().isoformat()
    }

    return jsonify({"result": "status updated"}), 200

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(latest_status), 200

# --------------------------------------------------
# Entry point (Render / local compatible)
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

