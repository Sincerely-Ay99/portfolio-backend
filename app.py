from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.json

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    msg = EmailMessage()
    msg["Subject"] = "New Portfolio Contact Message"
    msg["From"] = EMAIL_USER
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(
        f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return jsonify({"success": True})

    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to send message"}), 500


if __name__ == "__main__":
    app.run(debug=True)
