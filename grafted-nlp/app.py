import json
from trtr import *
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    if 'body' in event.keys():
        req = json.loads(event['body'])
    else:
        req = event
    logger.info("req ==================")
    logger.info(req)
    logger.info(type(req))
    if 'selectedTypes' not in req.keys():
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'error':'selected types not found'})
        }
    if 'doc' not in req.keys():
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'error':'content not found'})
        }
    resp = {}
    if 'keywords' in req['selectedTypes']:
        resp['keywords'] = extract_key_phrases(req["doc"])
    if 'summary' in req['selectedTypes']:
        resp["summary"] = extract_sentences(req["doc"])
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": json.dumps(resp)
    }