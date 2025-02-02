from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Telegram Mini-App Link Converter!"

@app.route('/redirect')
def redirect_to_telegram():
    invite_code = request.args.get('code')
    if invite_code:
        telegram_link = f"https://t.me/+{invite_code}"
        return redirect(telegram_link)
    return "Invalid invite code!", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
