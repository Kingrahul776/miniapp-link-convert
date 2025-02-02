from flask import Flask, request, render_template_string, jsonify
import random
import string
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)

# ✅ Secret Key for Encryption (Keep this the same across deployments)
SECRET_KEY = Fernet.generate_key()  # ⚠️ SAVE THIS KEY SECURELY
cipher = Fernet(SECRET_KEY)

# ✅ Temporary storage for encrypted short links
short_links = {}

# ✅ Generate a random short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ Encrypt the private link
def encrypt_link(private_link):
    encrypted_bytes = cipher.encrypt(private_link.encode())
    return base64.urlsafe_b64encode(encrypted_bytes).decode()

# ✅ Decrypt the private link
def decrypt_link(encrypted_data):
    decrypted_bytes = cipher.decrypt(base64.urlsafe_b64decode(encrypted_data))
    return decrypted_bytes.decode()

# ✅ API to create a short link (Encrypts the private link)
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

# ✅ Hide the redirection link using JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <script>
        function redirectToPrivateLink() {
            fetch('/get_private_link?code={{ short_code }}')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = data.private_link;  // ✅ Redirect using JavaScript
                    } else {
                        document.getElementById("status").innerText = "Invalid or Expired Link!";
                    }
                })
                .catch(() => {
                    document.getElementById("status").innerText = "Error occurred!";
                });
        }
        window.onload = redirectToPrivateLink;
    </script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; padding: 50px; }
        h1 { color: #007bff; }
        #status { font-size: 18px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Redirecting...</h1>
    <p id="status">Please wait...</p>
</body>
</html>
"""

# ✅ Route to retrieve the decrypted private link
@app.route('/get_private_link')
def get_private_link():
    short_code = request.args.get('code')

    encrypted_link = short_links.get(short_code)
    if not encrypted_link:
        return jsonify({"success": False, "message": "Invalid or expired link"}), 404

    decrypted_link = decrypt_link(encrypted_link)
    return jsonify({"success": True, "private_link": decrypted_link})

# ✅ Route to display the intermediate redirect page (Prevents showing real link in address bar)
@app.route('/<short_code>')
def redirect_to_private(short_code):
    return render_template_string(HTML_TEMPLATE, short_code=short_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
