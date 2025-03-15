# -*- coding=utf-8 -*-

import sys
import os
from dotenv import load_dotenv
import logging


def load_configurations(app):
    """
    Load configurations from the environment
    """
    if os.getenv('WEBSITE_HOSTNAME') is None:
        load_dotenv()
    app.config["ACCESS_TOKEN"] = os.getenv("ACCESS_TOKEN")
    app.config["YOUR_PHONE_NUMBER"] = os.getenv("YOUR_PHONE_NUMBER")
    app.config["APP_ID"] = os.getenv("APP_ID")
    app.config["APP_SECRET"] = os.getenv("APP_SECRET")
    app.config["RECIPIENT_WAID"] = os.getenv("RECIPIENT_WAID")
    app.config["VERSION"] = os.getenv("VERSION")
    app.config["PHONE_NUMBER_ID"] = os.getenv("PHONE_NUMBER_ID")
    app.config["VERIFY_TOKEN"] = os.getenv("VERIFY_TOKEN")
    logging.info("Configurations loaded")
    logging.info(f"Access token: {app.config['ACCESS_TOKEN'][:5]}*****")


def configure_logging(app):
    """
    Configure logging
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    # app.logger.addHandler(logging.StreamHandler(sys.stdout))
