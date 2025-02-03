import os
import json
import random
import string
import base64
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# ✅ Generate an encryption key (DO NOT CHANGE AFTER DEPLOYMENT)
SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

# ✅ Data storage (for demo purposes, use a database in production)
short_links = {}  # Stores encrypted links
subscriptions = {}  # Stores user subscriptions

# ✅ Generate a random short code
def generate_short_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ Encrypt a private link
def encrypt_link(private_link):
    encrypted_bytes = cipher.encrypt(private_link.encode())
    return base64.urlsafe_b64encode(encrypted_bytes).decode()

# ✅ Decrypt a private link
def decrypt_link(encrypted_data):
    decrypted_bytes = cipher.decrypt(base64.urlsafe_b64decode(encrypted_data))
    return decrypted_bytes.decode()

# ✅ Store an encrypted private link
@app.route('/store_link', methods=['POST'])
def store_link():
    data = request.json
    private_link = data.get("private_link")
    user_id = data.get("user_id")

    if not private_link or not user_id:
        return jsonify({"success": False, "message": "Invalid request!"}), 400

    # ✅ Check if the user has an active subscription
    if user_id not in subscriptions or subscriptions[user_id] < datetime.utcnow():
        return jsonify({"success": False, "message": "User does not have an active subscription!"}), 403

    encrypted_link = encrypt_link(private_link)
    short_code = generate_short_code()
    short_links[short_code] = encrypted_link

    short_url = f"https://t.me/vipsignals221bot?start={short_code}"  # Replace BOT2_USERNAME with actual bot username

    return jsonify({"success": True, "short_link": short_url})

# ✅ Retrieve an encrypted link for Bot 2
@app.route('/get_link', methods=['GET'])
def get_link():
    short_code = request.args.get("short_code")
    encrypted_link = short_links.get(short_code)

    if not encrypted_link:
        return jsonify({"success": False, "message": "Invalid or expired link!"}), 404

    decrypted_link = decrypt_link(encrypted_link)
    return jsonify({"success": True, "private_link": decrypted_link})

# ✅ Manually add a subscription (Admin only)
@app.route('/add_subscription', methods=['POST'])
def add_subscription():
    data = request.json
    user_id = str(data.get("user_id"))
    days = data.get("days", 30)

    if not user_id:
        return jsonify({"success": False, "message": "Invalid request!"}), 400

    expiry_date = datetime.utcnow() + timedelta(days=days)
    subscriptions[user_id] = expiry_date

    return jsonify({"success": True, "message": f"Subscription added for {user_id} until {expiry_date}."})

# ✅ Check if a user has an active subscription
@app.route('/check_subscription', methods=['GET'])
def check_subscription():
    user_id = request.args.get("user_id")

    if user_id in subscriptions and subscriptions[user_id] > datetime.utcnow():
        return jsonify({"success": True, "expiry_date": subscriptions[user_id].isoformat()})
    else:
        return jsonify({"success": False, "message": "No active subscription found."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
