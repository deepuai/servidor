import pika

def send_message_to_queue(queue, message):
    credencials = pika.PlainCredentials('deepuai', 'deepuai')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credencials))
    channel = connection.channel()
    channel.queue_declare(queue)
    channel.basic_publish(exchange='', routing_key=queue, body=message)
    connection.close()