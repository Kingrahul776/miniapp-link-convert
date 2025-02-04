from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# ✅ Secret key for encryption
SECRET_KEY = "supersecret"

# ✅ In-memory storage (Replace with Database)
subscriptions = {}
links = {}

# ✅ Admin User ID (Permanent Subscription)
ADMIN_ID = "6142725643"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running!"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/add_subscription", methods=["POST"])
def add_subscription():
    data = request.get_json()
    user_id = str(data.get("user_id"))

    # ✅ If admin user (6142725643), give permanent access
    if user_id == ADMIN_ID:
        subscriptions[user_id] = "PERMANENT"
        return jsonify({"message": f"Admin {user_id} has a permanent subscription.", "success": True}), 200

    # ✅ For regular users, set subscription expiry
    days = int(data.get("days", 30))
    expiry_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    subscriptions[user_id] = expiry_date

    return jsonify({
        "message": f"Subscription added for {user_id} until {expiry_date}.",
        "success": True
    }), 200

@app.route("/store_link", methods=["POST"])
def store_link():
    data = request.get_json()
    user_id = str(data.get("user_id"))

    # ✅ Check Subscription (Admins have permanent access)
    if user_id != ADMIN_ID and (user_id not in subscriptions or subscriptions[user_id] < datetime.datetime.utcnow()):
        return jsonify({"message": "User does not have an active subscription!", "success": False}), 403

    private_link = data.get("private_link")
    token = jwt.encode({"link": private_link}, SECRET_KEY, algorithm="HS256")
    
    short_link = f"https://t.me/vipsignals221bot?start={token}"
    links[token] = private_link
    
    return jsonify({"short_link": short_link, "success": True}), 200

@app.route("/redirect/<token>", methods=["GET"])
def redirect(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"redirect_to": decoded["link"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Link expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid link"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
