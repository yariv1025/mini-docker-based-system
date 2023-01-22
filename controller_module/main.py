import json
import logging
import os

from message_broker import Subscriber, Publisher

DELAY = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JSON_PATH = f"{os.path.abspath(os.getcwd())}/controller_module/output"


def to_json_file(new_data):
    """
    Writing data to a JSON file.
    Parameters
    ----------
    data - a new data to update
    """
    logger.info(f"Writing data to json file in: {JSON_PATH}")

    with open(f"{JSON_PATH}/modules_result.json", 'r') as fp:
        data = json.load(fp)

        logger.info(f"JSON load is: {data}")

    if "password" in new_data.keys():
        data["password_module"] = new_data
    else:
        data["analyze_module"] = new_data

    try:

        with open(f"{JSON_PATH}/modules_result.json", 'w') as fp:
            json.dump(data, fp, indent=4, sort_keys=True)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")

    logger.info(f"JSON after update is: {data}")


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

    logger.info(f"Output paths: {JSON_PATH}/modules_result.json")
    # os.chmod(os.getcwd(), 0o777)

    try:
        if not os.path.exists(JSON_PATH):
            logger.info(f"Creating a new DIR in: {JSON_PATH}")
            os.makedirs(JSON_PATH)

        with open(f"{JSON_PATH}/modules_result.json", 'x') as fp:
            logger.info(f"Writing the initial JSON data...")
            json.dump(json_body, fp, indent=4, sort_keys=True)

    except (OSError, FileExistsError, FileNotFoundError, PermissionError, IsADirectoryError) as e:
        logger.error(f"Exceprion: {str(e)}")


def get_config():
    try:
        abs_path = f"{os.path.abspath(os.getcwd())}/configuration/rabbitmq.config.json"
        logger.info(f"Read configuration from: {abs_path}")
        with open(abs_path, "r") as fp:
            return json.load(fp)

    except Exception as e:
        logger.error(f"{str(e)}")


if __name__ == '__main__':
    logger.info("Controller module is running...")

    # Configuration:
    logger.info("Create configuration")
    config = get_config()["rabbitmq"]
    password_module_config = {"queue_name": "password_mod_q", "routing_key": "password_mod_q"}
    analyze_module_config = {"queue_name": "analyze_mod_q", "routing_key": "analyze_mod_q"}
    controller_config = {"queue_name": "controller_mod_q", "routing_key": "controller_mod_q"}

    initialize_json_file()

    # Creating a publisher to triggering the modules by sending a message
    logger.info("Creating Publisher, and connection.")
    publisher = Publisher(config)
    publisher.health_check_rabbitmq()
    publisher.connect()

    logger.info(f"Publish 'Get analyze' to {analyze_module_config['routing_key']}")
    publisher.publish(analyze_module_config["routing_key"], "Get analyze")

    logger.info(f"Publish 'Get password' to {password_module_config['routing_key']}")
    publisher.publish(password_module_config["routing_key"], "Get password")

    # Creating a subscriber to get the data the modules returns
    logger.info("Creating Subscriber, and connection.")
    controller_mod_subscriber = Subscriber(config, controller_config["queue_name"], controller_config["routing_key"])
    controller_mod_subscriber.health_check_rabbitmq()
    controller_mod_subscriber.connect()

    logger.info("Consume the data.")
    controller_mod_subscriber.setup(callback=consume_callback)
    controller_mod_subscriber.setup(callback=consume_callback)

