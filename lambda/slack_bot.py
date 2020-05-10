import hashlib
import hmac
import json
import logging
import os
import urllib.request

SLACK_BOT_USER_ACCESS_TOKEN = os.environ["SLACK_BOT_USER_ACCESS_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("start")
    # 受信データを Cloud Watch Logs に出力しておく
    logger.info(json.dumps(event))

    # リクエスト署名のチェック
    if not is_valid_request(event):
        logger.warning("invalid request")
        return

    # Bot へのメンションじゃないときは何もしない
    e = json.loads(event["body"])
    if not is_app_mention(e):
        return

    # app_mention の処理
    process_app_mention(e)
    logger.info("end")


def is_valid_request(event):
    if "X-Slack-Request-Timestamp" not in event["headers"] \
            or "X-Slack-Signature" not in event["headers"]:
        return False

    expected_hash = generate_hmac_signature(
        event["headers"]["X-Slack-Request-Timestamp"],
        event["body"]
    )
    expected = "v0={}".format(expected_hash)
    actual = event["headers"]["X-Slack-Signature"]

    logger.debug("Expected HMAC signature: {}".format(expected))
    logger.debug("Actual HMAC signature: {}".format(actual))

    return hmac.compare_digest(expected, actual)


def generate_hmac_signature(timestamp, body):
    secret_key_bytes = bytes(SLACK_SIGNING_SECRET, 'UTF-8')

    message = "v0:{}:{}".format(timestamp, body)
    message_bytes = bytes(message, 'UTF-8')
    return hmac.new(secret_key_bytes, message_bytes, hashlib.sha256).hexdigest()


def is_app_mention(event):
    return event.get("event")["type"] == "app_mention"


def process_app_mention(event):
    e = event.get("event")
    tokens = e["text"].split(" ")[1:]
    if len(tokens) == 0:
        post_message_to_channel(e, "What?")
        return

    post_message_to_channel(e, " ".join(tokens))


def post_message_to_channel(event, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(SLACK_BOT_USER_ACCESS_TOKEN),
    }

    data = {
        "token": SLACK_BOT_USER_ACCESS_TOKEN,
        "channel": event["channel"],
        "text": get_user_mention(event["user"]) + " " + message,
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        logger.info(response_body)


def get_user_mention(user_id):
    return "<@" + user_id + ">"
