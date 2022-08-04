import pika


class MessageBroker:

    def __init__(self, config):
        self.config = config

    def create_connection(self):
        """
        Creating a new instance of the connection object

        Returns
        -------
        A new instance of the connection object
        """
        param = pika.ConnectionParameters(host=self.config['host'], port=self.config['port'])
        return pika.BlockingConnection(param)


class Publisher(MessageBroker):

    def __init__(self, config):
        super().__init__(config)

    def publish(self, routing_key, message):
        """
        Publish a message
        Parameters
        ----------
        routing_key: routing key
        message: the message we want to publish
        """
        connection = super().create_connection()
        channel = connection.channel()

        # Creates an exchange
        channel.exchange_declare(exchange=self.config['exchange'], exchange_type='topic')

        # Publishes message to the exchange with the given routing key
        channel.basic_publish(exchange=self.config['exchange'], routing_key=routing_key, body=message)
        print(f'[*] Sent message "{message}" to {routing_key}')


class Subscriber(MessageBroker):

    def __init__(self, queue_name, binding_key, config):
        super().__init__(config)
        self.queue_name = queue_name
        self.binding_key = binding_key
        self.connection = super().create_connection()

    def __del__(self):
        """
        Close the connection to the server
        """
        self.connection.close()

    def on_message_callback(self, channel, method, properties, body):
        """

        Parameters
        ----------
        method

        Returns
        -------

        """
        binding_key = method.routing_key
        print(f'[*] received new message for - {binding_key}')

    def setup(self, callback=(lambda *args, **kwargs: 1)):
        """
        Consume a new message from the appropriate queue
        """
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.config['exchange'], exchange_type='topic')

        # Creates or checks a queue
        channel.queue_declare(queue=self.queue_name)

        # Binds the queue to the specified exchange
        channel.queue_bind(queue=self.queue_name, exchange=self.config['exchange'], routing_key=self.binding_key)

        # channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message_callback, auto_ack=True)
        channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        print(f'[*] Waiting for data from {self.queue_name}. To exit press CTRL+C')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
