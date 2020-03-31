import datetime
import json
from uuid import uuid4

from aiohttp.web_response import json_response


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()

        try:
            return obj.tojson()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)


def stringified_uuid():
    return str(uuid4())


def serialize(data):
    return json.dumps(data, cls=JSONEncoder)


def jsonify(*args, **kwargs):
    return json_response(dumps=serialize, *args, **kwargs)
