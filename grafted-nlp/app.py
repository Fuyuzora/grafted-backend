import json
import logging
from trtr import *
from wiki_lookup import *
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    if 'body' in event.keys():
        req = json.loads(event['body'])
    else:
        req = event
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
        kws = extract_key_phrases(req["doc"])
        tagged_explained_kws = getIntroFromWiki(kws)
        resp['keywords'] = [{'header':kw, 'subheader':tag, 'content':info} for kw, tag, info in tagged_explained_kws]
    if 'summary' in req['selectedTypes']:
        resp["summary"] = [extract_sentences(req["doc"])]
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