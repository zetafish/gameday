#!/usr/bin/env python

import boto3
import json
import base64

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


def handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record["kinesis"]["data"])
        msg = json.loads(payload)
        msg_id = msg['Id']
        if not is_published(msg_id):
            store_message(msg)
