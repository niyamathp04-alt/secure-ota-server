from flask import Flask, jsonify, send_from_directory
import os
import json

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


# --------------------------------------------------
# Entry point (Render / local compatible)
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
