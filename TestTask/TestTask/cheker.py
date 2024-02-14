import json


def is_jsong(date):
    try:
        tup_json = json.loads(date)
        return tup_json
    except ValueError:
        return None
