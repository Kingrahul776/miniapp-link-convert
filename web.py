from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
CHANNEL_LINK = "https://t.me/+foDsQEgRiEU3N2E1"  # 🔹 Replace with your actual channel invite link
user_data = set()  # ✅ Store collected user IDs

@app.route('/')
def home():
    return "Welcome to the Telegram Mini-App Redirector!"

# ✅ Track user and redirect instantly
@app.route('/redirect')
def redirect_to_telegram():
    user_id = request.args.get('user_id')
    if user_id:
        user_data.add(user_id)  # ✅ Store user ID for future broadcasts
        return redirect(CHANNEL_LINK)
    return "Invalid request!", 400

# ✅ Get stored user IDs for broadcasting
@app.route('/get_users')
def get_users():
    return jsonify(list(user_data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
