# -*- coding=utf-8 -*-

import logging
import json
from flask import Blueprint, request, jsonify, current_app

from .decorators.security import signature_required
from .utils.whatsapp_utils import process_whatsapp_message, is_valid_whatsapp_message


webhook_blueprint = Blueprint("webhook", __name__)


def handle_message():
    """
    Handle incoming webhook events from the WhatsApp API.

    This function processes incoming WhatsApp messages and other events,
    such as delivery statuses. If the event is a valid message, it gets
    processed. If the incoming payload is not a recognized WhatsApp event,
    an error is returned.

    Every message send will trigger 4 HTTP requests to your webhook: message, sent, delivered, read.

    Returns:
        response: A tuple containing a JSON response and an HTTP status code.
    """
    body = request.get_json()
    logging.info(f"request body: {body}")

    # Check if it's a WhatsApp status update
    if (
        body.get('entry', [{}])[0]
        .get('chages', [{}])[0]
        .get('value', {})
        .get('statuses')
    ):
        logging.info('Received WhatsApp status update')
        return jsonify({'status': 'ok'}), 200

    try:
        if is_valid_whatsapp_message(body):
            process_whatsapp_message(body)
            return jsonify({'status': 'ok'}), 200
        else:
            return (
                jsonify({'status': 'error', 'message': 'Invalid WhatsApp message'}),
                404
            )
    except json.JSONDecodeError:
        logging.error('Failed to parse JSON payload')
        return (
            jsonify({'status': 'error', 'message': 'Invalid JSON payload'}),
            400
        )


# Required webhook verification for WhatsApp API
def verify():
    # Parse params from the webhook verification request
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == 'subscribe' and token == current_app.config['VERIFY_TOKEN']:
            # Respond with 200 OK and challenge token from the request
            logging.info('Webhook verified')
            return challenge, 200
        else:
            # Respond with 403 Forbidden if verify tokens do not match
            logging.error('Webhook verification failed')
            return jsonify({'status': 'error', 'message': 'Verification token mismatch'}), 403
    else:
        # Respond with 400 Bad Request if no verify token found
        logging.info('Missing parameters for webhook verification')
        return jsonify({'status': 'error', 'message': 'Missing verify token'}), 400


@webhook_blueprint.route('/webhook', methods=['GET'])
def webhook_get():
    return verify()


@webhook_blueprint.route('/webhook', methods=['POST'])
@signature_required
def webhook_post():
    return handle_message()
