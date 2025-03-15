#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
app_webhook.py
Description: This script handles webhook events for the Badminton Robot application.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Process the webhook data here
    if 'messages' in data:
        for message in data['messages']:
            if 'mentionedJidList' in message and 'your_bot_number@s.whatsapp.net' in message['mentionedJidList']:
                # Respond to the mention
                response_message = {
                    'to': message['from'],
                    'type': 'text',
                    'text': 'Hello! How can I assist you?'
                }
                # Send the response message (you need to implement the send_message function)
                # send_message(response_message)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(ports=8000)
