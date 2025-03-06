from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
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
    app.run(debug=True)


