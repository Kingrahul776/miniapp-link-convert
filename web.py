from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)
CHANNEL_LINK = "https://t.me/+foDsQEgRiEU3N2E1"  # 🔹 Replace with your actual channel invite link
user_data = set()  # ✅ Store collected user IDs

# ✅ HTML Page for the Mini-App
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join Our Channel</title>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; padding: 50px; }
        h1 { color: #007bff; }
        .btn { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; font-size: 18px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Welcome to Our Community!</h1>
    <p>Click the button below to join our Telegram channel.</p>
    <a class="btn" href="{{ channel_link }}">Join Channel</a>
</body>
</html>
"""

@app.route('/')
def home():
    return "Welcome to the Telegram Mini-App Redirector!"

# ✅ Store user ID and show the join button
@app.route('/redirect')
def redirect_to_telegram():
    user_id = request.args.get('user_id')
    if user_id:
        user_data.add(user_id)  # ✅ Store user ID for future broadcasts
        return render_template_string(HTML_TEMPLATE, channel_link=CHANNEL_LINK)
    return "Invalid request!", 400

# ✅ Get stored user IDs for broadcasting
@app.route('/get_users')
def get_users():
    return jsonify(list(user_data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
