import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CyberGuardianLogs')

def lambda_handler(event, context):
    response = table.scan()
    items = sorted(response['Items'], key=lambda x: x['timestamp'], reverse=True)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items, ensure_ascii=False)
    }