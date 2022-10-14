import os


class Config(object):
    wether_key = os.environ.get('WetherAPIKey')
