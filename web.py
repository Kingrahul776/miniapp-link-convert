from flask import Flask, request, jsonify, render_template
import jwt
import datetime

app = Flask(__name__)

# ✅ Secret key for encryption (MUST MATCH `bot1.py`)
SECRET_KEY = "supersecret"

# ✅ In-memory storage for demo (Replace with Database in production)
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
    private_link = data.get("private_link")

    # ✅ Validate request data
    if not private_link:
        return jsonify({"message": "Invalid request. No private link provided!", "success": False}), 400

    # ✅ Check Subscription
    if user_id not in subscriptions or subscriptions[user_id] < datetime.datetime.utcnow():
        return jsonify({"message": "User does not have an active subscription!", "success": False}), 403

    try:
        # ✅ Generate JWT token
        token = jwt.encode({"link": private_link}, SECRET_KEY, algorithm="HS256")
        short_link = f"https://www.kingcryptocalls.com/miniapp?start={token}"

        # ✅ Store the tokenized link
        links[token] = private_link

        return jsonify({"short_link": short_link, "success": True}), 200
    except Exception as e:
        return jsonify({"message": f"Error generating link: {str(e)}", "success": False}), 500

@app.route("/miniapp", methods=["GET"])
def miniapp():
    return render_template("miniapp.html")  # ✅ Mini-App frontend

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
