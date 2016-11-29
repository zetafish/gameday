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


# parsing arguments
#PARSER = argparse.ArgumentParser(description='Client message processor')
#PARSER.add_argument('API_token', help="the individual API token given to your team")
#PARSER.add_argument('API_base', help="the base URL for the game API")

api_token = 'adc1a51632'
api_base  ='https://dashboard.cash4code.net/score' 


#ARGS = PARSER.parse_args()

# defining global vars
MESSAGES = {} # A dictionary that contains message parts
#API_BASE = ARGS.API_base
# 'https://csm45mnow5.execute-api.us-west-2.amazonaws.com/dev'

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
    published.put_item(data)

    
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
    

    
def process_message(msg):
    """
    processes the messages by combining and appending the kind code
    """
    msg_id = msg['Id'] # The unique ID for this message
    part_number = msg['PartNumber'] # Which part of the message it is
    data = msg['Data'] # The data of the message

    # Try to get the parts of the message from the MESSAGES dictionary.
    # If it's not there, create one that has None in both parts
    parts = MESSAGES.get(msg_id, [None, None])

    # store this part of the message in the correct part of the list
    parts[part_number] = data

    # store the parts in MESSAGES
    MESSAGES[msg_id] = parts

    # if both parts are filled, the message is complete
    if None not in parts:
        # app.logger.debug("got a complete message for %s" % msg_id)
        print "have both parts"
        # We can build the final message.
        result = parts[0] + parts[1]
        # sending the response to the score calculator
        # format:
        #   url -> api_base/jFgwN4GvTB1D2QiQsQ8GHwQUbbIJBS6r7ko9RVthXCJqAiobMsLRmsuwZRQTlOEW
        #   headers -> x-gameday-token = API_token
        #   data -> EaXA2G8cVTj1LGuRgv8ZhaGMLpJN2IKBwC5eYzAPNlJwkN4Qu1DIaI3H1zyUdf1H5NITR
        
        app.logger.debug("ID: %s" % msg_id)
        app.logger.debug("RESULT: %s" % result)
        url = api_base + '/' + msg_id
        print url
        print result
        req = urllib2.Request(url, data=result, headers={
            'x-gameday-token': api_token,
            'content-type': 'application/text'
        })
        resp = urllib2.urlopen(req)
        resp.close()
        print resp

    return 'OK'

if __name__ == "__main__":

    api_base = 'http://localhost:8000'
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
    
