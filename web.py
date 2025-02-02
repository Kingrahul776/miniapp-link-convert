from flask import Flask, request, render_template_string, jsonify, redirect

app = Flask(__name__)
CHANNEL_LINK = "https://t.me/+foDsQEgRiEU3N2E1"  # 🔹 Replace with your actual channel invite link
user_data = {}  # ✅ Store collected user IDs

# ✅ Telegram Mini-App WebPage with Redirect Button
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join Our Channel</title>
    <script>
        function redirectToTelegram() {
            window.location.href = "{{ channel_link }}";
        }
        setTimeout(redirectToTelegram, 3000);  // ✅ Auto-redirect after 3 seconds
    </script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; padding: 50px; }
        h1 { color: #007bff; }
        .btn { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; font-size: 18px; border-radius: 5px; }
        #status { font-size: 16px; margin-bottom: 10px; color: green; }
    </style>
</head>
<body>
    <h1>Welcome to Our Community!</h1>
    <p id="status">Redirecting you to the Telegram channel...</p>
    <p>If you are not redirected, <a class="btn" href="{{ channel_link }}">Click Here</a></p>
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
        user_data[user_id] = "Joined"
        return render_template_string(HTML_TEMPLATE, channel_link=CHANNEL_LINK)
    return "Invalid request!", 400

# ✅ Get stored user IDs for broadcasting
@app.route('/get_users')
def get_users():
    return jsonify(list(user_data.keys()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
