import os
import json
import urllib3
from urllib.parse import urlparse, unquote
import logging
import requests

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info(json.dumps(event))

    o = urlparse(event["body"])
    path_splits = o.path.split("&")

    text = [s for s in path_splits if "text=" in s]
    token = [s for s in path_splits if "token=" in s]

    msg = text[0].split("=")[1]
    a_token = token[0].split("=")[1]

    msg = unquote(msg)
    token = unquote(a_token)

    if token == os.environ['access_token']:
        url = "https://slack.com/api/chat.postMessage"
        data = {
            "channel": os.environ['channel_id'],
            "text": msg,
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": os.environ['bot_token']
        }

        print(data)

        http = urllib3.PoolManager()
        req = http.request("POST",
                           url,
                           body=json.dumps(data).encode("utf-8"),
                           headers=headers,
                           )

        try:
            with urllib.request.urlopen(req) as res:
                return {"statusCode": 200, "body": ""}
        except urllib.error.HTTPError as err:
            print(err.code)
            return {"statusCode": 500, "body": ""}
        except urllib.error.URLError as err:
            print(err.reason)
            return {"statusCode": 500, "body": ""}

    return {"statusCode": 401, "body": ""}
