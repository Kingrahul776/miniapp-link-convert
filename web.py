from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# ✅ Secret Key for Encryption
SECRET_KEY = "supersecret"

# ✅ In-Memory Storage (Replace with DB)
subscriptions = {}
links = {}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/add_subscription", methods=["POST"])
def add_subscription():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    days = int(data.get("days", 30))
    
    expiry_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    subscriptions[user_id] = expiry_date
    
    return jsonify({"message": f"Subscription added for {user_id} until {expiry_date}.", "success": True}), 200

@app.route("/store_link", methods=["POST"])
def store_link():
    data = request.get_json()
    user_id = str(data.get("user_id"))

    if user_id != "6142725643" and (user_id not in subscriptions or subscriptions[user_id] < datetime.datetime.utcnow()):
        return jsonify({"message": "User does not have an active subscription!", "success": False}), 403

    private_link = data.get("private_link")
    token = jwt.encode({"link": private_link}, SECRET_KEY, algorithm="HS256")
    
    short_link = f"https://t.me/vipsignals221bot/start?startapp={token}"
    links[token] = private_link
    
    return jsonify({"short_link": short_link, "success": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
