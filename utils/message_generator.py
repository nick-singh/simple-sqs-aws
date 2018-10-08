from faker import Faker
import random, json

fake = Faker()

def gen_req(uuid, idx):
    return {
        'MessageAttributes':{
            'Title': {
                'DataType': 'String',
                'StringValue': fake.word()
            },
            'Author': {
                'DataType': 'String',
                'StringValue': fake.name()
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': str(random.randint(3,30))
            },
            'FileId':{
                'DataType': 'String',
                'StringValue':str(idx)
            }
        },

        'MessageBody':(
            fake.sentence()
        )
    }
