# -*- coding=utf-8 -*-

"""
security.py

This module contains security-related decorators for the WhatsAppRobot application.
"""

from functools import wraps
from flask import request, current_app, jsonify
import logging
import hashlib
import hmac


def validate_signature(payload, signature):
    """
    Validate the incoming payload's signature against our expected signature.
    """
    # Use the App Secret to hash the payload
    expected_signature = hmac.new(
        bytes(current_app.config['APP_SECRET'], 'latin-1'),
        msg=payload.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Check if the signatures matches
    return hmac.compare_digest(expected_signature, signature)


def signature_required(func):
    """
    Decorator to ensure that the user is authenticated before accessing the function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        signature = request.headers.get('X-Hub-Signature-256', '')[7:]
        if not validate_signature(request.data.decode('utf-8'), signature):
            logging.info('Signature validation failed')
            return jsonify({'status': 'error', 'message': 'Invalid signature'}), 403
        return func(*args, **kwargs)
    return wrapper
