import json
import pika, sys, os
sys.path.append('../..')
import src.utils.processing as processing

def fit_message_process(channel, method, properties, body):
    print('\n**********************************************')
    processing.fit(json.loads(body))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print('******** Finishing message processing ********')

def keep_consumer_opened(queue_name, callback):
    credencials = pika.PlainCredentials('deepuai', 'deepuai')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credencials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        keep_consumer_opened('fit', callback=fit_message_process)
    except Exception as e:
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)