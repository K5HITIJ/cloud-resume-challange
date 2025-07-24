import json
import boto3
import os
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'visitor-counter')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    Lambda function to handle visitor counter requests
    Supports both GET (get count) and POST (increment count) methods
    """
    
    try:
        # Get HTTP method
        http_method = event.get('httpMethod', 'GET')
        
        # Handle CORS preflight requests
        if http_method == 'OPTIONS':
            return create_response(200, {'message': 'OK'})
        
        if http_method == 'GET':
            # Get current visitor count without incrementing
            count = get_visitor_count()
        elif http_method == 'POST':
            # Increment and return visitor count
            count = increment_visitor_count()
        else:
            return create_response(405, {'error': 'Method not allowed'})
        
        return create_response(200, {
            'count': count,
            'visitor_count': count,
            'message': 'Success'
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_response(500, {
            'error': 'Internal server error',
            'message': str(e)
        })

def get_visitor_count():
    """Get the current visitor count from DynamoDB"""
    try:
        response = table.get_item(
            Key={'id': 'visitor_count'}
        )
        
        if 'Item' in response:
            return int(response['Item']['count'])
        else:
            # If item doesn't exist, create it with count 0
            table.put_item(
                Item={
                    'id': 'visitor_count',
                    'count': 0
                }
            )
            return 0
            
    except ClientError as e:
        print(f"Error getting visitor count: {e}")
        raise e

def increment_visitor_count():
    """Increment the visitor count in DynamoDB and return the new count"""
    try:
        response = table.update_item(
            Key={'id': 'visitor_count'},
            UpdateExpression='ADD #count :inc',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        
        return int(response['Attributes']['count'])
        
    except ClientError as e:
        print(f"Error incrementing visitor count: {e}")
        # If item doesn't exist, create it
        if e.response['Error']['Code'] == 'ValidationException':
            table.put_item(
                Item={
                    'id': 'visitor_count',
                    'count': 1
                }
            )
            return 1
        raise e

def create_response(status_code, body):
    """Create a properly formatted HTTP response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body, default=decimal_default)
    }

def decimal_default(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError
