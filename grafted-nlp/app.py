import json
from trtr import *

setup_environment()

def handler(event, context):
    resp = {}
    if 'keywords' in event.keys():
        resp['keywords'] = extract_key_phrases(event["keywords"])
    if 'summary' in event.keys():
        resp["summary"] = extract_sentences(event["summary"])
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(resp)
    }