import json
import pika, sys, os
sys.path.append('../..')
import src.utils.processing as processing

def callback(ch, method, properties, body):
    processing.fit(json.loads(body))

def keep_consumer_opened():
    credencials = pika.PlainCredentials('deepuai', 'deepuai')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credencials))
    queue_name = 'fit'
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        keep_consumer_opened()
    except Exception as e:
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)