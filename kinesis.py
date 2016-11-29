#!/usr/bin/env python

import boto3
import json
import base64

api_token = 'adc1a51632'
api_base  ='https://dashboard.cash4code.net/score'


dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
pending = dynamodb.Table('pending')
published = dynamodb.Table('published')


def store_message(msg):
    pending.put_item(Item=msg)


def is_published(msg_id):
    key = {
        'Id': msg_id
    }
    response = published.get_item(Key=key)
    return 'Item' in response


def mark_published(msg_id):
    data = {
        'Id': msg_id
    }
    published.put_item(Item=data)


def resolve(msg):
    msg_id = msg['Id']
    total = msg['TotalNumbers']
    data = ''
    for i in range(total):
        response = pending.get_item(Key={'Id': msg_id, 'PartNumber': i})
        if 'Item' not in response:
            return None

        part = response['Item']
        data = data + part['Data']

    return data


def publish(msg_id, data):
    url = api_base + '/' + msg_id
    headers = {'x-gameday-token': api_token}
    urllib2.Request(url, data=data, headers=headers)


def handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record["kinesis"]["data"])
        msg = json.loads(payload)
        msg_id = msg['Id']
        if not is_published(msg_id):
            store_message(msg)
            data = resolve(msg)
            if data:
                publish(msg_id, data)
