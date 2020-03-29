import pika

class RabbitMQ:
  def __init__(self, host, port):
    params = pika.ConnectionParameters(host, port)
    self.connection = pika.BlockingConnection(params)
    self.channel = self.connection.channel()

  def declare_queue(self, queue_name):
    self.channel.queue_declare(queue=queue_name, exclusive=True)

  def declare_broadcast_queue(self, queue_name):
    self.channel.exchange_declare(exchange=queue_name, exchange_type='fanout')

  def publish_to_queue(self, queue_name, routing_key, message):
    self.channel.basic_publish(exchange=queue_name,
                    routing_key=routing_key,
                    body=message)
    
  def bind_queue_to_exchange(self, queue_name, exchange_name):
    self.channel.queue_bind(exchange=exchange_name,
                 queue=queue_name)

  def consume_from_queue(self, queue_name, callback):
    self.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    self.channel.start_consuming()

  def close(self):
    self.connection.close()



