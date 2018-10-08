import boto3
from utils import message_generator
import os, json, uuid
import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('config.ini')

# Create SQS client
sqs = boto3.client('sqs')

queue_url = settings.get('AcccessKeys', 'queue_url')


num_msgs = 100

for i,x in enumerate(range(0,num_msgs)[:1]):
    file_name = str(uuid.uuid1())
    data = message_generator.gen_req(file_name, i)
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes=data['MessageAttributes'],
        MessageBody=data['MessageBody']
    )

    print(i, response['MessageId'])



#
# response = sqs.send_message(
#     QueueUrl=queue_url,
#     DelaySeconds=10,
#     MessageAttributes={
#         'Title': {
#             'DataType': 'String',
#             'StringValue': 'The Whistler'
#         },
#         'Author': {
#             'DataType': 'String',
#             'StringValue': 'John Grisham'
#         },
#         'WeeksOn': {
#             'DataType': 'Number',
#             'StringValue': '6'
#         }
#     },
#     MessageBody=(
#         'Information about current NY Times fiction bestseller for '
#         'week of 12/11/2016.'
#     )
# )
