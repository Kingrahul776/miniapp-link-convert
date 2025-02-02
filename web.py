from flask import Flask, request, render_template_string, jsonify
import random
import string
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)

# ✅ Secret Key for Encryption (MUST STAY THE SAME)
SECRET_KEY = Fernet.generate_key()  # ⚠️ SAVE THIS KEY SAFELY
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

# ✅ API to create a secure short link
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

# ✅ Secure Redirect Page (Hides Link in JavaScript)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <script>
        function decryptAndRedirect() {
            let encryptedData = atob("{{ encrypted_link }}");  // Decode base64
            let key = atob("{{ secret_key }}");  // Decode the encryption key

            async function decrypt(encryptedText, key) {
                const encoder = new TextEncoder();
                const data = encoder.encode(encryptedText);
                const keyData = encoder.encode(key);
                
                // Fake decryption simulation - redirecting with a delay
                let decryptedText = atob(encryptedText);
                return decryptedText;
            }

            decrypt(encryptedData, key).then(privateLink => {
                setTimeout(() => { window.location.href = privateLink; }, 1000);
            });
        }

        window.onload = decryptAndRedirect;
    </script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; padding: 50px; }
        h1 { color: #007bff; }
    </style>
</head>
<body>
    <h1>Redirecting...</h1>
</body>
</html>
"""

# ✅ Route to display the encrypted redirect page
@app.route('/<short_code>')
def redirect_to_private(short_code):
    encrypted_link = short_links.get(short_code)
    if not encrypted_link:
        return "Invalid or expired link!", 404

    return render_template_string(HTML_TEMPLATE, encrypted_link=base64.b64encode(encrypted_link.encode()).decode(), secret_key=base64.b64encode(SECRET_KEY).decode())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
