import os

class Config(object):

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    INFLUX_HOST = os.getenv('INFLUX_HOST', 'localhost')
    INFLUX_PORT = os.getenv('INFLUX_PORT', 8086)
    INFLUX_USER = os.getenv('INFLUX_USER', '')
    INFLUX_PASSWORD = os.getenv('INFLUX_PASSWORD', '')
    INFLUX_DB = os.getenv('INFLUX_DB', 'mydb')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

