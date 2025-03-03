import json
import boto3
import os
import datetime  # Import datetime for timestamp logging

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    current_time = datetime.datetime.now().isoformat() # Get timestamp for logs
    print(f"STARTING LAMBDA INVOCATION - Timestamp: {current_time}") # Log at start

    try:
        print(f"  [LOG] - {current_time} - Getting item from DynamoDB...") # Log before DynamoDB get
        response = table.get_item(Key={'id': 'visitor_count'})
        print(f"  [LOG] - {current_time} - DynamoDB GetItem Response: {response}") # Log DynamoDB response

        if 'Item' not in response:
            current_count = 0
            print(f"  [LOG] - {current_time} - Item not found, initializing count to 0") # Log if item not found
        else:
            current_count = int(response['Item']['count'])
            print(f"  [LOG] - {current_time} - Retrieved current count: {current_count}") # Log retrieved count

        updated_count = current_count + 1
        print(f"  [LOG] - {current_time} - Incrementing count to: {updated_count}") # Log before incrementing

        print(f"  [LOG] - {current_time} - Putting item to DynamoDB with count: {updated_count}...") # Log before DynamoDB put
        table.put_item(Item={'id': 'visitor_count', 'count': updated_count})
        print(f"  [LOG] - {current_time} - DynamoDB PutItem completed.") # Log after DynamoDB put

        api_response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET"
            },
            "body": json.dumps({"count": updated_count})
        }
        print(f"  [LOG] - {current_time} - Lambda function completed SUCCESSFULLY. Response: {api_response}") # Log on success
        return api_response

    except Exception as e:
        print(f"  [ERROR] - {current_time} - Exception occurred: {e}") # Log any exceptions
        api_response = {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET"
            },
            "body": json.dumps({"error": str(e)})
        }
        print(f"  [LOG] - {current_time} - Lambda function completed with ERROR. Response: {api_response}") # Log on error
        return api_response
    finally:
        print(f"ENDING LAMBDA INVOCATION - Timestamp: {current_time}") # Log at end