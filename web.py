from flask import Flask, request, jsonify
import random
import string
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)

# ✅ Generate and store an encryption key (DO NOT CHANGE AFTER DEPLOYMENT)
SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

# ✅ Temporary storage for encrypted links
short_links = {}

# ✅ Generate a random short code
def generate_short_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ Encrypt the private link
def encrypt_link(private_link):
    encrypted_bytes = cipher.encrypt(private_link.encode())
    return base64.urlsafe_b64encode(encrypted_bytes).decode()

# ✅ Decrypt the private link
def decrypt_link(encrypted_data):
    decrypted_bytes = cipher.decrypt(base64.urlsafe_b64decode(encrypted_data))
    return decrypted_bytes.decode()

# ✅ Store the encrypted link
@app.route('/store_link', methods=['POST'])
def store_link():
    data = request.json
    private_link = data.get("private_link")

    if not private_link:
        return jsonify({"success": False, "message": "Invalid request! No private link provided."}), 400

    encrypted_link = encrypt_link(private_link)
    short_code = generate_short_code()
    short_links[short_code] = encrypted_link

    short_url = f"https://t.me/vipsignals221bot?start={short_code}"  # Redirect via Bot 2

    return jsonify({"success": True, "short_link": short_url})

# ✅ Retrieve and decrypt the stored private link for Bot 2
@app.route('/get_link', methods=['GET'])
def get_link():
    short_code = request.args.get("short_code")
    encrypted_link = short_links.get(short_code)

    if not encrypted_link:
        return jsonify({"success": False, "message": "Invalid or expired link"}), 404

    decrypted_link = decrypt_link(encrypted_link)
    return jsonify({"success": True, "private_link": decrypted_link})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
