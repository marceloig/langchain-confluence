
import os
import requests
import boto3
import json
from ytmusicapi import YTMusic
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):
    
    try:
        logger.info(event)
        
        ytmusic = YTMusic("oauth.json")

    except Exception as e:
        logger.error(e)
        raise e