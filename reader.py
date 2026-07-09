import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("statusping-results")


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError


def lambda_handler(event, context):
    urls_to_check = [
        "https://www.google.com",
        "https://www.github.com"
    ]

    all_results = []

    for url in urls_to_check:
        response = table.query(
            KeyConditionExpression=Key("url").eq(url),
            ScanIndexForward=False,
            Limit=1
        )
        items = response.get("Items", [])
        if items:
            all_results.append(items[0])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(all_results, default=decimal_default)
    }