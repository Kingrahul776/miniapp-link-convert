from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)
CHANNEL_LINK = "https://t.me/+foDsQEgRiEU3N2E1"  # 🔹 Replace with your actual channel invite link
user_data = {}  # ✅ Store collected user IDs

# ✅ Mini-App HTML with Auto-Redirect to Telegram Channel
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        function openChannel() {
            Telegram.WebApp.openTelegramLink("{{ channel_link }}");
        }
        setTimeout(openChannel, 1000);  // ✅ Auto-redirect after 1 second
    </script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; padding: 50px; }
        h1 { color: #007bff; }
        .btn { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; font-size: 18px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Redirecting...</h1>
    <p>If you are not redirected automatically, <a class="btn" onclick="openChannel()">Click Here</a></p>
</body>
</html>
"""

@app.route('/')
def home():
    return "Welcome to the Telegram Mini-App Redirector!"

# ✅ Store user ID and open the channel inside Telegram
@app.route('/redirect')
def redirect_to_telegram():
    user_id = request.args.get('user_id')
    if user_id:
        user_data[user_id] = "Joined"
        return render_template_string(HTML_TEMPLATE, channel_link=CHANNEL_LINK)
    return "Invalid request!", 400

# ✅ Get stored user IDs for broadcasting
@app.route('/get_users')
def get_users():
    return jsonify(list(user_data.keys()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
