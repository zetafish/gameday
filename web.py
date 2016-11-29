#!/usr/bin/env python
import urllib2
import boto3
import json


# dynamodb
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
pending = dynamodb.Table('pending')
published = dynamodb.Table('published')

# api
api_token = 'adc1a51632'
api_base  ='https://dashboard.cash4code.net/score' 


def store_message(msg):
    pending.put_item(Item=msg)

def resolve(msg):
    msg_id = msg['Id']
    total = msg['TotalParts']
    data = ''
    for i in range(total):
        response = pending.get_item(Key={'Id': msg_id, 'PartNumber': i})
        if 'Item' not in response:
            return None

        part = response['Item']
        data = data + part['Data']

    return data

def mark_published(msg_id):
    data = {
        'Id': msg_id
    }
    published.put_item(Item=data)

    
def is_published(msg_id):
    key = {
        'Id': msg_id
    }
    response = published.get_item(Key=key)
    return 'Item' in response


def process_message(msg):
    msg_id = msg['Id']

    if not is_published(msg_id):
        store_message(msg)
        data = resolve(msg)
        if data is not None:
            publish(msg_id, data)
            mark_published(msg)


def handler(event, context):
    msg = event
    process_message(msg)
    # op = event['operation']
    # if op == 'create':
    #     payload = event.get('payload')
    #     msg = json.loads(payload)
    #     process_message(msg)
