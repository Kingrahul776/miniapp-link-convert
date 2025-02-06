from flask import Flask, request, jsonify, redirect
import jwt
import datetime
import logging

app = Flask(__name__)

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Secret key for encryption (Same as Bot 1)
SECRET_KEY = "supersecret"

# ✅ In-memory storage (Replace with a database)
subscriptions = {"6142725643": datetime.datetime.utcnow() + datetime.timedelta(days=9999)}  # Admin has lifetime access
links = {}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running!"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/store_link", methods=["POST"])
def store_link():
    data = request.get_json()
    user_id = str(data.get("user_id"))

    # ✅ Check Subscription
    if user_id not in subscriptions or subscriptions[user_id] < datetime.datetime.utcnow():
        return jsonify({"message": "User does not have an active subscription!", "success": False}), 403

    private_link = data.get("private_link")
    token = jwt.encode({"link": private_link}, SECRET_KEY, algorithm="HS256")
    
    # ✅ Generate Mini App link
    short_link = f"https://www.kingcryptocalls.com/miniapp?start={token}"
    links[token] = private_link

    return jsonify({"short_link": short_link, "success": True}), 200

# ✅ Mini App Page (Redirect to Telegram)
@app.route("/miniapp", methods=["GET"])
def miniapp():
    token = request.args.get("start")

    if not token:
        return "❌ Invalid request. No token provided.", 400

    try:
        # ✅ Decode the token
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        channel_invite_link = decoded_data["link"]

        # ✅ 🚀 Redirect user to Telegram invite link
        return redirect(channel_invite_link, code=302)
    except jwt.ExpiredSignatureError:
        return "❌ Error: Link expired.", 403
    except jwt.InvalidTokenError:
        return "❌ Error: Invalid link.", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
