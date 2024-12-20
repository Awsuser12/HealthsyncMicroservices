from flask import Flask, request, jsonify
import smtplib

app = Flask(__name__)

@app.route('/send_reminder', methods=['POST'])
def send_reminder():
    """Send a reminder email."""
    data = request.json
    email = data.get('email')
    message = data.get('message')
    
    try:
        # Mock email sending
        print(f"Sending email to {email} with message: {message}")
        return jsonify({"message": "Reminder sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
