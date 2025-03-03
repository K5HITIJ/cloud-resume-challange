import json
import boto3
import os

# Initialize DynamoDB client - using boto3, the AWS SDK for Python
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME') # Get table name from environment variable
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    '''
    This function handles the HTTP GET request, retrieves the count from DynamoDB,
    increments it, and returns the updated count.
    '''
    try:
        # Get the current count from DynamoDB
        response = table.get_item(Key={'id': 'visitor_count'}) # 'id' is our partition key

        if 'Item' not in response:
            current_count = 0 # Initialize count if item doesn't exist yet
        else:
            current_count = int(response['Item']['count'])

        # Increment the count
        updated_count = current_count + 1

        # Update the count in DynamoDB
        table.put_item(Item={'id': 'visitor_count', 'count': updated_count})

        # Construct the response to be sent back to the frontend
        api_response = {
            "statusCode": 200, # HTTP status code for success
            "headers": {
                "Content-Type": "application/json", # Indicate JSON response
                "Access-Control-Allow-Origin": "*", # Allow cross-origin requests (for website to call API)
                "Access-Control-Allow-Methods": "GET" # Allow only GET requests
            },
            "body": json.dumps({ # Convert Python dictionary to JSON string
                "count": updated_count
            })
        }

        return api_response

    except Exception as e:
        # Handle any errors and return an error response
        api_response = {
            "statusCode": 500, # HTTP status code for server error
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET"
            },
            "body": json.dumps({
                "error": str(e) # Return error message in JSON
            })
        }
        return api_response