from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
short_links = {}  # Stores short links in memory (use a database for production)

@app.route('/')
def home():
    return "Welcome to KingCryptoCalls Telegram Mini-App Shortener!"

# Store a new short link
@app.route('/store', methods=['POST'])
def store_link():
    data = request.json
    short_code = data.get("code")
    target_url = data.get("target")

    if short_code and target_url:
        short_links[short_code] = target_url
        return jsonify({"message": "Short link stored!"}), 200
    return jsonify({"error": "Invalid data"}), 400

# Redirect from short link to Telegram
@app.route('/<short_code>')
def redirect_link(short_code):
    target_url = short_links.get(short_code)
    if target_url:
        return redirect(target_url)
    return "Invalid link!", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
