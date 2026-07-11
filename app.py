from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = "abc123"  # Đặt cứng

@app.route('/webhook', methods=['GET'])
def verify():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        return challenge
    return "Verification failed", 403

@app.route('/')
def home():
    return "Webhook is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
