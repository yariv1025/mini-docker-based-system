import json
import logging
import os

from message_broker import Subscriber, Publisher
from services.scanner_service import ScannerService

DELAY = 10
SEARCH_PATH = f"{os.path.abspath(os.getcwd())}/theHarvester"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_top_10_files():
    """
    Finding the number of files from each type (e.g. .py, .txt, etc...)
    Returns
    -------
    top 10 files sorted by size
    """
    logger.info(f'Looking for the top 10 files types in {SEARCH_PATH}')
    extensions = ScannerService.find_extension(SEARCH_PATH)
    return list(extensions)[:10]


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
    logger.info(f'[*] received new message in - {binding_key}')

    # produce a new message
    logger.info(f'Creating publisher...')
    publisher = Publisher(config)
    publisher.health_check_rabbitmq()
    publisher.connect()

    message = json.dumps({"files_types": find_top_10_files()})
    logger.info(f'The 10 top files are: {message}')

    logger.info(f'Publishing to {controller_config["routing_key"]}')
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
    logger.info("Analyze module is listening...")

    # Configuration:
    config = get_config()["rabbitmq"]
    analyze_module_config = {"queue_name": "analyze_mod_q", "routing_key": "analyze_mod_q"}

    # Creating a subscriber for consuming a messages
    analyze_mod_subscriber = Subscriber(config,
                                        analyze_module_config["queue_name"],
                                        analyze_module_config["routing_key"])
    analyze_mod_subscriber.health_check_rabbitmq()
    analyze_mod_subscriber.connect()

    analyze_mod_subscriber.setup(callback=on_message_callback)
