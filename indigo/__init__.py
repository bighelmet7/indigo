from flask import Flask

app_config = dict() # Global app configuration, doesnt need any context to be executed.

def create_app(config_obj='consultant.config.DevelopmentConfig'):
    """
    Returns an app Flask object configurated with the given config_obj.
    """
    global app_config

    app = Flask(__name__)
    app.config.from_object(config_obj)
    app_config = app.config.copy()

    from v2.blueprint import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v2')

    from flask_cors import CORS
    CORS(app)

    return app

def create_db_client():
    '''
    Returns a setted influxdb client with the given configuration.
    '''
    config = app_config
    from influxdb import InfluxDBClient

    client = InfluxDBClient(
        host=config.get('INFLUX_HOST'),
        port=config.get('INFLUX_PORT'),
        username=config.get('INFLUX_USER'),
        password=config.get('INFLUX_PASSWORD'),
        database=config.get('INFLUX_DB'),
    )
    return client

