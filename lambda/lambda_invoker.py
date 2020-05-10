import json
import boto3
import logging
import os

FUNCTION_NAME = os.environ["INVOCATION_FUNCTION_NAME"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("start")
    # 受信データを Cloud Watch Logs に出力しておく
    logging.info(json.dumps(event))

    e = json.loads(event["body"])
    if "challenge" in e:
        return {
            "statusCode": 200,
            "body": json.dumps(e["challenge"])
        }

    client = boto3.client("lambda")
    client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="Event",
        LogType="Tail",
        Payload=json.dumps(event)
    )

    logger.info("end")
    return {
        "statusCode": 200,
        "body": json.dumps("OK")
    }
