import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('dynamo_table')

def lambda_handler(event, context):
    print('Request event: ', event)
    response = None
    if event['httpMethod'] == 'GET' and event['path'] == '/health':
        response = build_response(200)
    elif event['httpMethod'] == 'GET' and event['path'] == '/product':
        response = get_product(event['queryStringParameters']['pk'])
    elif event['httpMethod'] == 'GET' and event['path'] == '/products':
        response = get_products()
    elif event['httpMethod'] == 'POST' and event['path'] == '/product':
        response = save_product(json.loads(event['body']))
    elif event['httpMethod'] == 'PATCH' and event['path'] == '/product':
        request_body = json.loads(event['body'])
        response = modify_product(request_body['pk'], request_body['updateKey'], request_body['updateValue'])
    elif event['httpMethod'] == 'DELETE' and event['path'] == '/product':
        response = delete_product(json.loads(event['body'])['pk'])
    else:
        response = build_response(404, '404 Not Found')
    return response

def get_product(product_id):
    try:
        response = table.get_item(Key={'pk': product_id})
        return build_response(200, response['Item'])
    except Exception as e:
        print('Do your custom error handling here. I am just gonna log it:', e)

def get_products():
    try:
        scan_params = {'TableName': 'dynamo_table'}
        response = table.scan(**scan_params)
        products = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            products.extend(response['Items'])
        return build_response(200, {'products': products})
    except Exception as e:
        print('Do your custom error handling here. I am just gonna log it:', e)

def save_product(request_body):
    try:
        table.put_item(Item=request_body)
        return build_response(200, {'Operation': 'SAVE', 'Message': 'SUCCESS', 'Item': request_body})
    except Exception as e:
        print('Do your custom error handling here. I am just gonna log it:', e)

def modify_product(product_id, update_key, update_value):
    try:
        response = table.update_item(
            Key={'pk': product_id},
            UpdateExpression=f'set {update_key} = :value',
            ExpressionAttributeValues={':value': update_value},
            ReturnValues='UPDATED_NEW'
        )
        return build_response(200, {'Operation': 'UPDATE', 'Message': 'SUCCESS', 'UpdatedAttributes': response})
    except Exception as e:
        print('Do your custom error handling here. I am just gonna log it:', e)

def delete_product(product_id):
    try:
        response = table.delete_item(Key={'pk': product_id}, ReturnValues='ALL_OLD')
        return build_response(200, {'Operation': 'DELETE', 'Message': 'SUCCESS', 'Item': response})
    except Exception as e:
        print('Do your custom error handling here. I am just gonna log it:', e)

def build_response(status_code, body=None):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body) if body is not None else None
    }
