#!/usr/bin/env python

import time
import json
import sys
import tweepy
import slackweb
import configparser
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

def read_config(filename = 'twitter.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    data = {}
    for key in config['config']:
        data[key] = config['config'][key]
    return data

def read_twitter_id(filename = 'twitter.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    data = []
    for key in config['id']:
        data.append(config['id'][key])
    return data

def get_auth():
    cfg = read_config()
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return auth

def get_api():
    return tweepy.API(get_auth())

def get_slack():
    return slackweb.Slack(url=read_config('slack.ini')['webhook'])

class StdOutListener(StreamListener):

    def on_data(self, data):
        if 'delete' in json.loads(data):
            return True
        if 'RT' in json.loads(data)['text']:
            return True
        if str(json.loads(data)['user']['id']) in ids:
            slack = get_slack()
            print(data)
            slack.notify(text=json.loads(data)['text'])
            return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    stream = Stream(get_auth(), l)
    stream.filter(follow=read_twitter_id())
