import requests
import hashlib
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# -----------------------------
# Device current firmware version
# -----------------------------
current_version = 1  # Change this to simulate "update available" or "up to date"

# Server metadata URL
metadata_url = "http://127.0.0.1:8000/metadata"

# Local public key for signature verification
public_key_path = "../signer/public_key.pem"

update_available = False
firmware_data = b''
firmware_hash = ''
firmware_signature = ''

def fetch_metadata():
    global update_available, firmware_data, firmware_hash, firmware_signature
    print("🔍 Checking for firmware update...")
    try:
        response = requests.get(metadata_url)
        response.raise_for_status()
        metadata = response.json()
    except Exception as e:
        print("❌ Error fetching update:", e)
        return False

    server_version = metadata.get("version", 0)
    print(f"📌 Latest Version on Server: {server_version}")

    if server_version > current_version:
        print("⬇ Update available!")
        update_available = True
        firmware_url = metadata.get("url")
        firmware_hash = metadata.get("hash")
        firmware_signature = metadata.get("signature")
        return True
    else:
        print("✅ Up to date")
        update_available = False
        return False

def update_now():
    global current_version, update_available
    if not update_available:
        print("⚠ No update available to download.")
        return

    firmware_url = metadata_url.replace("metadata", "firmware/firmware_v2.bin")
    print("⬇ Downloading firmware...")
    try:
        data = requests.get(firmware_url).content
    except Exception as e:
        print("❌ Error downloading firmware:", e)
        return

    print("🔐 Verifying Hash...")
    sha256 = hashlib.sha256(data).digest()
    hash_base64 = base64.b64encode(sha256).decode()

    if hash_base64 == firmware_hash:
        print("✅ Hash Verified Successfully.")
    else:
        print("❌ Hash verification failed!")
        return

    print("🔏 Verifying Signature...")
    try:
        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        signature_bytes = base64.b64decode(firmware_signature)
        public_key.verify(
            signature_bytes,
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("✅ Signature Verified Successfully.")
        current_version += 1
        update_available = False
        print("🎉 Firmware updated successfully. Current version:", current_version)
    except Exception as e:
        print("❌ Signature verification failed!", e)

# -----------------------------
# Main flow
# -----------------------------
if fetch_metadata():
    user_input = input("Do you want to update now? (y/n): ")
    if user_input.lower() == 'y':
        update_now()
    else:
        print("Update postponed by user.")
