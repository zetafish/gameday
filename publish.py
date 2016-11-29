#!/usr/bin/env python
"""
Client which receives the requests

Args:
    API Token
    API Base (https://...)

"""
from flask import Flask, request
import logging
import argparse
import urllib2
import boto3

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger('server')

# dynamodb
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
pending = dynamodb.Table('pending')
published = dynamodb.Table('published')

# api
api_token = 'adc1a51632'
api_base  ='https://dashboard.cash4code.net/score' 


def handler(event, context):
    records = event['Records']
    for r in records:
        event_name = r['eventName']
        if event_name == 'INSERT':
            d = r['dynamodb']
            keys = data['Keys']
            new = data['NewImage']
            


# defining global vars
MESSAGES = {} # A dictionary that contains message parts

app = Flask(__name__)

def store_message(msg):
    pending.put_item(Item=msg)

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


# creating flask route for type argument
@app.route('/', methods=['GET', 'POST'])
def main_handler():
    """
    main routing for requests
    """
    if request.method == 'POST':
        msg = request.get_json()
        process_message_dynamodb(msg)
        return "OK"
    else:
        return get_message_stats()

    
def get_message_stats():
    """
    provides a status that players can check
    """
    msg_count = len(MESSAGES.keys())
    return "There are %d messages in the MESSAGES dictionary" % msg_count


def process_message_dynamodb(msg):
    msg_id = msg['Id']
    
    if is_published(msg_id):
        return
    
    store_message(msg)
    data = resolve(msg)
    if data is not None:
        publish(msg_id, data)
        mark_published(msg_id)
        

def publish(msg_id, data):
    url = api_base + '/' + msg_id
    headers = {'x-gameday-token': api_token}
    urllib2.Request(url, data=data, headers=headers)
    
