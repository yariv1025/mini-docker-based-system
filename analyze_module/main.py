import json
import logging
import os

import messageBroker
from services.scanner_service import ScannerService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_top_10_files(search_path):
    """
    Finding the number of files from each type (e.g. .py, .txt, etc...)
    Returns
    -------
    top 10 files sorted by size
    """
    logger.info('Looking for the top 10 files types.')
    extensions = ScannerService.find_extension(search_path)
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
    print(f'[*] received new message in - {binding_key}')

    # produce a new message
    publisher = messageBroker.Publisher(config)
    message = json.dumps({"files_types": find_top_10_files(search_path)})
    publisher.publish(controller_config["routing_key"], message)


if __name__ == '__main__':
    logger.info("Analyze module is listening...")

    # Configuration:
    search_path = "../theHarvester"
    config = {'host': os.environ["rabbitmq_host"], 'port': os.environ["rabbitmq_port"], 'exchange': 'exchange'}
    analyze_module_config = {"queue_name": "analyze_mod_q", "routing_key": "analyze_mod_q"}

    # Creating a subscriber for consuming a messages
    analyze_mod_subscriber = messageBroker.Subscriber(analyze_module_config["queue_name"], analyze_module_config["routing_key"], config)
    analyze_mod_subscriber.setup(callback=on_message_callback)
