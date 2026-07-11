#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# KHOIVIDEV - MESSENGER WEBHOOK (Deploy sẵn sàng)

import os
import json
import requests
from flask import Flask, request, jsonify
from datetime import datetime

# ================== CẤU HÌNH ==================
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "EAAOfqZCjfjccBR9P926VEJINb81KZAEdvgnsI3xmflPgwyuyGaCV1FGHvlcCZAJElxKnQoCA99L65WFE6QTljQwsgeo82gRbwbrQGziBE9fml1w3EQZAOddVgKyZC6obvMcSKpTZCY3kaIcLOMCdDaZB5w1e8qtihZAhspSIroblPYRSUpiJpUQEkpjSa7lerHTRhrJ2M0EGZAwZDZD")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "khoividev")  # Tự đặt, phải khớp với Facebook
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

# ================== LOG ==================
def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

# ================== GỬI TIN NHẮN ==================
def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v20.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    try:
        response = requests.post(url, params=params, json=data, timeout=10)
        if response.status_code == 200:
            log(f"✅ Đã gửi tin nhắn đến {recipient_id}")
            return True
        else:
            log(f"❌ Lỗi gửi: {response.text}")
            return False
    except Exception as e:
        log(f"❌ Lỗi: {str(e)}")
        return False

def send_typing(recipient_id):
    url = "https://graph.facebook.com/v20.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {
        "recipient": {"id": recipient_id},
        "sender_action": "typing_on"
    }
    try:
        requests.post(url, params=params, json=data, timeout=5)
    except:
        pass

# ================== XỬ LÝ TIN NHẮN ==================
def handle_message(sender_id, message_text):
    log(f"📩 Tin nhắn từ {sender_id}: {message_text[:50]}...")
    send_typing(sender_id)
    
    # Logic đơn giản
    msg_lower = message_text.lower()
    
    if "xin chào" in msg_lower or "hello" in msg_lower:
        reply = "Xin chào! Tôi là bot tự động. Tôi có thể giúp gì cho bạn?"
    elif "cảm ơn" in msg_lower or "thanks" in msg_lower:
        reply = "Không có gì! Rất vui được giúp bạn 😊"
    elif "tạm biệt" in msg_lower or "bye" in msg_lower:
        reply = "Tạm biệt! Hẹn gặp lại bạn sau."
    elif "thời gian" in msg_lower or "giờ" in msg_lower:
        now = datetime.now().strftime("%H:%M:%S ngày %d/%m/%Y")
        reply = f"🕐 Hiện tại là: {now}"
    else:
        reply = "Cảm ơn bạn đã nhắn tin! Tôi sẽ trả lời bạn sớm nhất có thể."
    
    send_message(sender_id, reply)

def handle_postback(sender_id, payload):
    log(f"🔘 Postback từ {sender_id}: {payload}")
    if payload == "START":
        reply = "Chào mừng bạn! Bạn có thể bắt đầu chat với tôi."
    elif payload == "HELP":
        reply = "Tôi có thể giúp bạn: chào hỏi, hỏi giờ, cảm ơn, tạm biệt."
    else:
        reply = f"Bạn đã chọn: {payload}"
    send_message(sender_id, reply)

# ================== WEBHOOK ==================
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return "OK", 200
    
    try:
        entry = data.get('entry', [])[0]
        messaging = entry.get('messaging', [])
        
        for event in messaging:
            sender_id = event.get('sender', {}).get('id')
            if not sender_id:
                continue
            
            if 'message' in event and 'text' in event['message']:
                message_text = event['message']['text']
                handle_message(sender_id, message_text)
            elif 'postback' in event:
                payload = event['postback'].get('payload', '')
                handle_postback(sender_id, payload)
    except Exception as e:
        log(f"❌ Lỗi webhook: {str(e)}")
    
    return "OK", 200

# ================== ROUTE CHÍNH ==================
@app.route('/')
def home():
    return "🚀 Messenger Webhook đang chạy! URL: /webhook"

@app.route('/send', methods=['POST'])
def manual_send():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400
    user_id = data.get('user_id')
    message = data.get('message')
    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400
    success = send_message(user_id, message)
    return jsonify({"success": success})

# ================== CHẠY ==================
if __name__ == '__main__':
    print("=" * 50)
    print("🚀 KHOIVIDEV - MESSENGER WEBHOOK")
    print("=" * 50)
    print(f"📌 Verify Token: {VERIFY_TOKEN}")
    print(f"📌 Token: {PAGE_ACCESS_TOKEN[:20]}...")
    print(f"📌 Webhook URL: https://your-domain.com/webhook")
    print("=" * 50)
    app.run(host='0.0.0.0', port=PORT, debug=False)
