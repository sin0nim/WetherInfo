import os


class Config(object):
    wether_key = os.environ.get('WetherAPIKey')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-name-is-yury'
