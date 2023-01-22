import logging
import pika
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageBroker:

    def __init__(self, config):
        logger.info(f"Initialize Message Broker...")
        self.conf = config
        self.host = self.conf["host"]
        self.port = self.conf["port"]
        self.exchange = self.conf["exchange"]
        self.credentials = self.conf["credentials"]
        self.connection = None

    def connect(self):
        """
        Creating a new instance of the connection object

        Returns
        -------
            A new instance of the connection object
        """
        logger.info(f"Connecting...")

        credentials = pika.PlainCredentials(self.credentials["username"], self.credentials["password"])
        param = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(param)
        return self.connection

    def __del__(self):
        """
        Close the connection to the server
        """
        logger.info(f"Close connection...")
        if self.connection:
            self.connection.close()

    def health_check_rabbitmq(self):
        """
        Checking for connection
        """
        logger.info(f"Performing Health check...")

        while True:
            try:
                connection = self.connect()
                connection.close()
                logger.info(f"Health check succeeded...")
                break

            except Exception as e:
                logger.error(f"Rabbitmq is not up and running.")
                time.sleep(1)
                continue


class Publisher(MessageBroker):

    def __init__(self, config):
        logger.info(f"Initialize Publisher...")
        super().__init__(config)

    def publish(self, routing_key, message):
        """
        Publish a message
        Parameters
        ----------
        routing_key: routing key
        message: the message we want to publish
        """
        logger.info(f"Publishing...")
        channel = self.connection.channel()

        # Creates an exchange
        channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        # Publishes message to the exchange with the given routing key
        channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=message)
        print(f'[*] Sent message "{message}" to {routing_key}')


class Subscriber(MessageBroker):

    def __init__(self, config, queue_name, binding_key):
        logger.info(f"Initialize Subscriber...")
        super().__init__(config)
        self.queue_name = queue_name
        self.binding_key = binding_key

    def on_message_callback(self, channel, method, properties, body):
        """

        Parameters
        ----------
            method - ???

        """
        binding_key = method.routing_key
        logger.info(f'[*] received new message for - {binding_key}')

    def setup(self, callback=(lambda *args, **kwargs: 1)):
        """
        Consume a new message from the appropriate queue
        """
        logger.info(f"Subscriber Consume...")
        channel = self.connection.channel()

        # Creates an exchange
        channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        # Creates or checks a queue
        channel.queue_declare(queue=self.queue_name)

        # Binds the queue to the specified exchange
        channel.queue_bind(queue=self.queue_name, exchange=self.exchange, routing_key=self.binding_key)

        # channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message_callback, auto_ack=True)
        channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        print(f'[*] Waiting for data from {self.queue_name}. To exit press CTRL+C')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
