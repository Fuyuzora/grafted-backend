import json
from trtr import *

def handler(event, context):
    if 'selectedTypes' not in event.keys():
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'error':'selected types not found'})
        }
    if 'doc' not in event.keys():
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'error':'content not found'})
        }
    resp = {}
    if 'keywords' in event['selectedTypes']:
        resp['keywords'] = extract_key_phrases(event["doc"])
    if 'summary' in event['selectedTypes']:
        resp["summary"] = extract_sentences(event["doc"])
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(resp)
    }