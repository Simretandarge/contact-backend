from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure environment variables exist
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

if not EMAIL_USER or not EMAIL_PASS:
    raise ValueError("EMAIL_USER or EMAIL_PASS is missing from environment variables!")

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = EMAIL_USER
app.config['MAIL_PASSWORD'] = EMAIL_PASS
app.config['MAIL_DEFAULT_SENDER'] = EMAIL_USER

mail = Mail(app)

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json

        # Validate request data
        if not data or not all(key in data for key in ['name', 'email', 'message']):
            return jsonify({"message": "Invalid request, missing required fields"}), 400

        msg = Message(
            subject=f"New Contact Form Submission from {data['name']}",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=["andargesimret@gmail.com"],  # Change if needed
            body=f"Name: {data['name']}\nEmail: {data['email']}\nMessage: {data['message']}"
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"})

    except Exception as e:
        print("Email Error:", str(e))  # Debugging
        return jsonify({"message": "Failed to send email.", "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000
    app.run(host="0.0.0.0", port=port)
