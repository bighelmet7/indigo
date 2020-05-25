from flask import Blueprint
from flask_restful import Api


from v2.resources.database import DatabaseListResource,\
    DatabaseRetrieveResource, MeasurementResource, TagListResource,\
    TagRetrieveResource
from v2.resources.influx import InfluxResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

### INFLUX ENDPOINTS ###
api.add_resource(InfluxResource, '/influx/')

### Database endpoints ###
api.add_resource(DatabaseListResource, '/database/')
api.add_resource(DatabaseRetrieveResource, '/database/<string:name>/')
api.add_resource(MeasurementResource, '/database/<string:db_name>/measurement/<string:measurement>/')
api.add_resource(TagListResource, '/database/<string:db_name>/measurement/<string:measurement>/tags/')
api.add_resource(TagRetrieveResource, '/database/<string:db_name>/measurement/<string:measurement>/tags/<string:tag_key>/')