from flask import Flask, request, jsonify, redirect
import random
import string
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)

# ✅ Generate a secret key for encryption (MUST STAY THE SAME ACROSS DEPLOYMENTS)
SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

# ✅ Temporary storage for encrypted short links
short_links = {}

# ✅ Generate a random short code
def generate_short_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ Encrypt the private link
def encrypt_link(private_link):
    encrypted_bytes = cipher.encrypt(private_link.encode())
    return base64.urlsafe_b64encode(encrypted_bytes).decode()

# ✅ Decrypt the private link
def decrypt_link(encrypted_data):
    decrypted_bytes = cipher.decrypt(base64.urlsafe_b64decode(encrypted_data))
    return decrypted_bytes.decode()

# ✅ API to create a secure short link (Encrypts the private link)
@app.route('/create_link', methods=['POST'])
def create_short_link():
    data = request.json
    private_link = data.get("private_link")

    if not private_link:
        return jsonify({"success": False, "message": "Invalid request! No private link provided."}), 400

    # ✅ Encrypt the private link
    encrypted_link = encrypt_link(private_link)

    # ✅ Generate a unique short code
    short_code = generate_short_code()
    short_links[short_code] = encrypted_link

    short_url = f"https://web-production-8fdb0.up.railway.app/{short_code}"
    return jsonify({"success": True, "short_link": short_url})

# ✅ Route to securely redirect without exposing the real link
@app.route('/<short_code>')
def redirect_to_private(short_code):
    encrypted_link = short_links.get(short_code)

    if not encrypted_link:
        return "Invalid or expired link!", 404

    # ✅ Decrypt the link securely on the server
    decrypted_link = decrypt_link(encrypted_link)

    return redirect(decrypted_link, code=302)  # ✅ Server-side redirection (NO LINK EXPOSURE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
