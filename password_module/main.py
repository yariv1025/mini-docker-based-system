import json
import logging
import os

from message_broker import Publisher, Subscriber
from services.scanner_service import ScannerService

DELAY = 10
SEARCH_PATH = f"{os.path.abspath(os.getcwd())}/theHarvester"
SEARCH_STR = "password"

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
    publisher = Publisher(config)
    publisher.health_check_rabbitmq()
    publisher.connect()

    message = json.dumps({"password": extract_password(SEARCH_STR, SEARCH_PATH)})
    logger.info(f'The password that found is: {message}')

    publisher.publish(controller_config["routing_key"], message)


def get_config():
    try:
        abs_path = f"{os.path.abspath(os.getcwd())}/configuration/rabbitmq.config.json"
        logger.info(f"Read configuration from: {abs_path}")
        with open(abs_path, "r") as fp:
            return json.load(fp)

    except Exception as e:
        logger.error(f"{str(e)}")


if __name__ == '__main__':
    logger.info("Password module is listening...")

    # Configuration:
    config = get_config()["rabbitmq"]
    password_module_config = {"queue_name": "password_mod_q", "routing_key": "password_mod_q"}

    # Creating a subscriber for consuming a messages
    password_mod_subscriber = Subscriber(config,
                                         password_module_config["queue_name"],
                                         password_module_config["routing_key"])

    password_mod_subscriber.health_check_rabbitmq()
    password_mod_subscriber.connect()

    password_mod_subscriber.setup(callback=on_message_callback)
