import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    # Get current count
    try:
        response = table.get_item(Key={'id': 'visitors'})
        count = response.get('Item', {}).get('count', 0)
    except:
        count = 0
    
    # Increment if POST
    if event.get('httpMethod') == 'POST':
        count += 1
        table.put_item(Item={'id': 'visitors', 'count': count})
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'count': count})
    }
