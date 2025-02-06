from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ✅ Secret key for encryption
SECRET_KEY = "supersecret"

# ✅ In-memory storage (Replace with a database)
subscriptions = {"6142725643": datetime.datetime.utcnow() + datetime.timedelta(days=9999)}  # Admin has lifetime access
links = {}

@app.route("/store_link", methods=["POST"])
def store_link():
    data = request.get_json()
    user_id = str(data.get("user_id"))

    # ✅ Check Subscription
    if user_id not in subscriptions or subscriptions[user_id] < datetime.datetime.utcnow():
        return jsonify({"message": "User does not have an active subscription!", "success": False}), 403

    private_link = data.get("private_link")
    token = jwt.encode({"link": private_link}, SECRET_KEY, algorithm="HS256")
    short_link = f"https://www.kingcryptocalls.com/miniapp?start={token}"

    links[token] = private_link
    return jsonify({"short_link": short_link, "success": True}), 200

# ✅ Serve the Mini App Frontend
@app.route("/miniapp", methods=["GET"])
def miniapp():
    return jsonify({"message": "🚀 MiniApp Loaded Successfully! Please provide access to continue."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
