from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

FIRMWARE_FOLDER = os.path.join(os.path.dirname(__file__), '../firmware')

# Serve metadata
@app.route('/metadata')
def metadata():
    import json
    with open('metadata.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

# Serve firmware files
@app.route('/firmware/<path:filename>')
def firmware(filename):
    return send_from_directory(FIRMWARE_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
