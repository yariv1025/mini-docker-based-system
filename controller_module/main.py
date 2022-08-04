import json
import logging
import os

from messageBroker import Subscriber, Publisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JSON_PATH = "../modules_result.json"


# def exec_to_json(search_path, search_str):
#     """
#     Execute the other modules and output the results (from both modules) to a json file.
#     Returns
#     -------
#     results as JSON file
#     """
#     result = {
#         "password": extract_password(search_str, search_path),
#         "top_10": find_top_10_files(search_path)
#     }
#
#     return json.dumps(result,
#                       indent=4,
#                       sort_keys=True)

def to_json_file(new_data):
    """
    Writing data to a JSON file.
    Parameters
    ----------
    data - a new data to update
    """
    logger.info("Writing data to json file...")

    with open(JSON_PATH, 'r') as fp:
        data = json.load(fp)

    if "password" in new_data.keys():
        data["password_module"] = new_data
    else:
        data["analyze_module"] = new_data

    with open(JSON_PATH, 'w') as fp:
        json.dump(data, fp)

    logger.info(f"Current json file: {json.dump(data)}")


def consume_callback(channel, method, properties, body):
    """
    Callback function
    Parameters
    ----------
    channel - channel object
    method - Basic.Deliver object
    properties - BasicProperties object
    body - the message from queue
    """
    logger.info("Callback activated.")

    binding_key = method.routing_key
    print(f'Body type: {type(body)}')
    print(f'[*] received new message in - {binding_key}:\n{body}')
    to_json_file(json.loads(body))


def initialize_json_file():
    """
    Preparing the json file
    """
    logger.info("Preparing the json file...")

    json_body = {
        "password_module": "",
        "analyze_module": ""
    }

    with open(JSON_PATH, 'w') as fp:
        json.dump(json_body, fp)


if __name__ == '__main__':
    logger.info("Controller module is running and listening...")

    # Message Broker configuration:
    config = {'host': os.environ["rabbitmq_host"], 'port': os.environ["rabbitmq_port"], 'exchange': 'exchange'}
    password_module_config = {"queue_name": "password_mod_q", "routing_key": "password_mod_q"}
    analyze_module_config = {"queue_name": "analyze_mod_q", "routing_key": "analyze_mod_q"}
    controller_config = {"queue_name": "controller_mod_q", "routing_key": "controller_mod_q"}

    initialize_json_file()

    # Creating a publisher to triggering the modules by sending a message
    publisher = Publisher(config)
    publisher.publish(analyze_module_config["routing_key"], "Get analyze")
    publisher.publish(password_module_config["routing_key"], "Get password")

    # Creating a subscriber to get the data the modules returns
    controller_mod_subscriber = Subscriber(controller_config["queue_name"], controller_config["routing_key"], config)
    controller_mod_subscriber.setup(callback=consume_callback)
