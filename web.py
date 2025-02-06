from flask import Flask, request, jsonify, render_template, redirect
import jwt
import datetime

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

@app.route("/miniapp", methods=["GET"])
def miniapp():
    return render_template("miniapp.html")  # ✅ Serve the Mini App frontend

@app.route("/redirect", methods=["GET"])
def redirect_to_channel():
    token = request.args.get("start")
    
    if not token:
        return "❌ Invalid token", 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        channel_link = decoded.get("link")
        return redirect(channel_link, code=302)  # ✅ Redirect to Telegram Channel
    except jwt.ExpiredSignatureError:
        return "❌ Link Expired", 403
    except jwt.InvalidTokenError:
        return "❌ Invalid Link", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
