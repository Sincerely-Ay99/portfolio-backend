from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import resend

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

app = Flask(__name__)
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=False
)

RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


@app.route("/api/ping", methods=["GET", "POST"])
def ping():
    return jsonify({"ok": True})


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.json

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    try:
        resend.Emails.send({
            "from": SENDER_EMAIL,
            "to": RECEIVER_EMAIL,
            "subject": "New Portfolio Contact Message",
            "text": f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        })
        return jsonify({"success": True})

    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to send message"}), 500


if __name__ == "__main__":
    app.run(debug=True)
