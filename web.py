from flask import Flask, request, jsonify, render_template, redirect
import jwt
import datetime

app = Flask(__name__)

# Secret key for encryption (Make sure this matches Bot 1)
SECRET_KEY = "supersecret"

# In-memory storage (Replace with Database in production)
subscriptions = {}
links = {}

# ✅ Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running!"}), 200

# ✅ Health Check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

# ✅ Add Subscription
@app.route("/add_subscription", methods=["POST"])
def add_subscription():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    days = int(data.get("days", 30))
    
    expiry_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    subscriptions[user_id] = expiry_date
    
    return jsonify({"message": f"Subscription added for {user_id} until {expiry_date}.", "success": True}), 200

# ✅ Store Link & Generate Encrypted Link
@app.route("/store_link", methods=["POST"])
def store_link():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    
    # Check Subscription
    if user_id not in subscriptions or subscriptions[user_id] < datetime.datetime.utcnow():
        return jsonify({"message": "User does not have an active subscription!", "success": False}), 403

    private_link = data.get("private_link")
    token = jwt.encode({"link": private_link}, SECRET_KEY, algorithm="HS256")
    
    short_link = f"https://t.me/vipsignals221bot?start={token}"
    links[token] = private_link
    
    return jsonify({"short_link": short_link, "success": True}), 200

# ✅ Redirect User After Decoding Token
@app.route("/redirect/<token>", methods=["GET"])
def redirect_user(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"redirect_to": decoded["link"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Link expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid link"}), 403

# ✅ Mini App Page (For Granting Permission)
@app.route("/miniapp", methods=["GET"])
def miniapp():
    start_param = request.args.get("start")

    if not start_param:
        return "<h2>Invalid request! No link found.</h2>", 400

    bot2_username = "vipsignals221bot"  # Your Bot 2 username
    return render_template("miniapp.html", start_param=start_param, bot2_username=bot2_username)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
