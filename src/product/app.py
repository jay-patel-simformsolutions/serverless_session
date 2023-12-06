from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import os
import json
import boto3
from utils import convert_dynamodb_json_to_readable

# Initialize the DynamoDB client
dynamodb = boto3.client("dynamodb")

app = APIGatewayRestResolver()

@app.post("/product/create")
def add_product():
    # Get the table name from the environment variable
    table_name = os.environ["TABLE_NAME"]

    # Parse the input JSON payload
    request_body = json.loads(app.current_event.body)

    # Extract product details from the request
    product_name = request_body.get("productName")
    product_description = request_body.get("productDescription")
    product_price = request_body.get("productPrice")

    # Check if required fields are provided
    if not product_name or not product_price:
        return {
            "statusCode": 400,
            "body": "productName and productPrice are required fields.",
        }

    # Generate a unique product ID (you can use a more sophisticated method)
    product_id = str(hash(product_name + product_description))

    # Create a new product item in DynamoDB
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "productId": {"S": product_id},
            "productName": {"S": product_name},
            "productDescription": {"S": product_description},
            "productPrice": {"N": str(product_price)},
        },
    )

    return "Successfully Created"



@app.get("/product/list")
def get_products():
    try:
        # Get the table name from the environment variable
        table_name = os.environ["TABLE_NAME"]

        # Scan the DynamoDB table to fetch all entries
        response = dynamodb.scan(TableName=table_name)

        # Extract the items from the response
        items = response.get("Items", [])

        # Convert the items to a list of dictionaries
        product_list = convert_dynamodb_json_to_readable(items)

        return product_list
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}


@app.get("/product/nested-loop")
def nested_loop():
    for i in range(10000):
        for i in range(10000):
            pass
    return "COMPLETED"


def lambda_handler(event, context):
    return app.resolve(event, context)
