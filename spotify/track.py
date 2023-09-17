
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

        #validate(event)
        
        if not event.get('next_track'):
            return event

        return
    except Exception as e:
        logger.error(e)
        raise e

def build_tracks(tracks, items):
    if not tracks:
        tracks = []

    for item in items:
        tracks.append(item['tracks']['href'])
    
    return tracks

def save_playlists(table_name, spotify, items):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    response = spotify.get("https://api.spotify.com/v1/me")
    user = response.json()
    user_id = user['id']
    
    for item in items:
        item['pk'] = 'SPOTIFY#' + user_id
        item['sk'] = 'PLAYLIST#' + item['id']
        table.put_item(
            Item=item
        )
        save_tracks(table_name, spotify, item)

def save_tracks(table_name, spotify, playlist):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    response = spotify.get("https://api.spotify.com/v1/me")
    user = response.json()
    user_id = user['id']
    response = spotify.get(playlist['tracks']['href'])
    data = response.json()
    print(json.dumps(data))

    for item in data['items']:
        if not item['track'].get('id'):
            continue

        item['pk'] = 'SPOTIFY#' + user_id
        item['sk'] = playlist['id'] + '#' + item['track']['id']
        table.put_item(
            Item=item
        )


def validate(event):
    if event.get('next_track') == None:
        raise Exception("Attribute 'next_track' have been present with string value")
    if not event.get('next_track'):
        raise Exception("Attribute 'next_track' not have been empty string")

def build_next(data):
    return data.get('next')

class Spotify:
    def __init__(self, access_token):
        self.headers = {"Authorization": "Bearer " + access_token}
        
    def get(self, url):
        return requests.get(url, headers=self.headers)