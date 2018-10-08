import boto3
from multiprocessing import Process, Queue, Pool, cpu_count

import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('config.ini')

# Create SQS client
sqs = boto3.client('sqs')

queue_url = settings.get('AcccessKeys', 'queue_url')

message_template = """
Title: {m[MessageAttributes][Title][StringValue]},
Author: {m[MessageAttributes][Author][StringValue]},
WeeksOn: {m[MessageAttributes][WeeksOn][StringValue]}
MessageBody: {m[Body]}
ID: {m[MessageAttributes][FileId][StringValue]}
"""

def process_msg(n):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    if 'Messages' in response.keys():
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        output = message_template.format(m=message)

        # print(output, receipt_handle)

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message:\n%s' % output)
        return receipt_handle
    else:
        return 0

single_processing = False

if single_processing:
    for i in range(10):
        process_msg(i)
else:
    while True:
        pool = Pool(cpu_count() * 10)
        all_results = pool.map(process_msg, range(10))

        pool.close()
        pool.join()

        print(len(all_results))

        if 0 in all_results:
            break
