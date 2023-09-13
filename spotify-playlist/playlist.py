
import os
import requests
import boto3
import json
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):
    
    try:
        logger.info(event)
        table_name = os.environ["TABLE_NAME"]

        validate(event)

        next = event.get('next')
        headers = {"Authorization": "Bearer " + event.get('access_token')}

        response = requests.get(next, headers=headers)
        if response.status_code != 200:
            logger.error(f"Error: Request returned status code {response.status_code}")
            raise Exception(response.text)
        
        data = response.json()

        response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        user = response.json()

        save_playlists(table_name, user['id'], data['items'])
        
        if data.get('next') == None:
            return {}
        
        output = {
            'next': build_next(data), 
            'access_token': event.get('access_token')
            }

        return output
    except Exception as e:
        logger.error(e)
        raise e

def save_playlists(table_name, user_id, items):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    for item in items:
        item['pk'] = 'spotify#' + user_id
        item['sk'] = item['name']
        table.put_item(
            Item=item
        )

def validate(event):
    if event.get('next') == None:
        raise Exception("Attribute 'next' have been present with string value")
    if not event.get('next'):
        raise Exception("Attribute 'next' not have been empty string")

def build_next(data):
    return data.get('next')
