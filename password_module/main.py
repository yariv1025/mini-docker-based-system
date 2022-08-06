import json
import logging
import os
import time

import messageBroker

from services.scanner_service import ScannerService

DELAY = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_password(search_str, search_path) -> str:
    """
    Extracting password
    Returns
    -------
    password
    """
    return ScannerService.find_string(search_str, search_path)[0][12:]


def on_message_callback(channel, method, properties, body):
    """
    Callback function
    Parameters
    ----------
    channel - channel object
    method - Basic.Deliver object
    properties - BasicProperties object
    body - the message from queue
    """

    controller_config = {"queue_name": "controller_mod_q", "routing_key": "controller_mod_q"}

    binding_key = method.routing_key
    print(f'[*] received new message in - {binding_key}')

    # produce a new message
    publisher = messageBroker.Publisher(config)
    publisher.health_check_rabbitmq()
    publisher.create_connection()

    message = json.dumps({"password": extract_password(search_str, search_path)})
    publisher.publish(controller_config["routing_key"], message)


if __name__ == '__main__':
    logger.info("Password module is listening...")

    # Configuration:
    search_path = "../theHarvester"
    search_str = "password"
    config = {'host': os.getenv("rabbitmq_host"), 'port': os.getenv("rabbitmq_port"), 'exchange': 'exchange'}
    password_module_config = {"queue_name": "password_mod_q", "routing_key": "password_mod_q"}

    # Creating a subscriber for consuming a messages
    password_mod_subscriber = messageBroker.Subscriber(password_module_config["queue_name"],
                                                       password_module_config["routing_key"], config)

    password_mod_subscriber.health_check_rabbitmq()
    password_mod_subscriber.create_connection()

    password_mod_subscriber.setup(callback=on_message_callback)
