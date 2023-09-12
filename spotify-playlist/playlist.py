
import os
import requests
import boto3
import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):
    
    try:
        logger.info(event)
        host = os.environ["HOST"]
        username = os.environ["USERNAME"]
        api_token = os.environ["API_TOKEN"]

        validate(event)

        next = event.get('next')

        response = requests.get(
            next,
            auth=(username, api_token),
            )
        if response.status_code != 200:
            logger.error(f"Error: Request returned status code {response.status_code}")
            raise Exception(response.text)
        
        data = response.json()
        
        if data.get('next') == None:
            return {}
        
        output = {'next': build_next(data)}

        return output
    except Exception as e:
        logger.error(e)
        raise e

def validate(event):
    if event.get('next') == None:
        raise Exception("Attribute 'next' have been present with string value")
    if not event.get('next'):
        raise Exception("Attribute 'next' not have been empty string")

def build_next(data):
    return data.get('next')
