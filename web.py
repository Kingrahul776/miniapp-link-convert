from flask import Flask, request, jsonify, render_template
import jwt
import datetime
import logging

app = Flask(__name__)

# ✅ Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Secret Key for JWT Encoding/Decoding
SECRET_KEY = "supersecret"

# ✅ In-Memory Storage (Replace with a database)
subscriptions = {
    "6142725643": datetime.datetime.utcnow() + datetime.timedelta(days=9999)  # ✅ Admin has lifetime access
}
links = {}

# ✅ Store Link & Generate MiniApp URL
@app.route("/store_link", methods=["POST"])
def store_link():
    try:
        data = request.get_json()
        user_id = str(data.get("user_id"))

        # ✅ Check Subscription
        if user_id not in subscriptions or subscriptions[user_id] < datetime.datetime.utcnow():
            logger.warning(f"❌ User {user_id} does not have an active subscription.")
            return jsonify({"message": "User does not have an active subscription!", "success": False}), 403

        private_link = data.get("private_link")

        if not private_link:
            logger.error("❌ No private link provided!")
            return jsonify({"message": "Invalid request, no link provided!", "success": False}), 400

        # ✅ Encode the link into JWT
        token = jwt.encode({"link": private_link}, SECRET_KEY, algorithm="HS256")
        short_link = f"https://www.kingcryptocalls.com/miniapp?start={token}"

        # ✅ Store the tokenized link
        links[token] = private_link

        logger.info(f"✅ Short link generated for user {user_id}: {short_link}")
        return jsonify({"short_link": short_link, "success": True}), 200

    except Exception as e:
        logger.error(f"❌ Error in /store_link: {str(e)}")
        return jsonify({"message": "Server error while generating link!", "success": False}), 500

# ✅ Mini App Page (Frontend)
@app.route("/miniapp", methods=["GET"])
def miniapp():
    return render_template("miniapp.html")  # ✅ Serve MiniApp Page

# ✅ Add Subscription API (For Admin or Manual Use)
@app.route("/add_subscription", methods=["POST"])
def add_subscription():
    try:
        data = request.get_json()
        user_id = str(data.get("user_id"))
        days = int(data.get("days", 30))

        expiry_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
        subscriptions[user_id] = expiry_date

        logger.info(f"✅ Subscription added for {user_id} until {expiry_date}.")
        return jsonify({"message": f"Subscription added for {user_id} until {expiry_date}.", "success": True}), 200

    except Exception as e:
        logger.error(f"❌ Error in /add_subscription: {str(e)}")
        return jsonify({"message": "Server error while adding subscription!", "success": False}), 500

# ✅ Start the Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
