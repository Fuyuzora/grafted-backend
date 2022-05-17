import json
from trtr import *
from parser import *

setup_environment()

def lambda_hander(event, context):
    resp = {}
    if event["keywords"]:
        resp['keywords'] = extract_key_phrases(event["keywords"])
    if event["summary"]:
        resp["summary"] = extract_sentences(event["summary"])
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(resp)
    }