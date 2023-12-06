from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import os
import json
import boto3
from utils import convert_dynamodb_json_to_readable

# Initialize the DynamoDB client
dynamodb = boto3.client("dynamodb")
sqs = boto3.client("sqs")

app = APIGatewayRestResolver()


def push_message_on_notification_queue(message: dict):
        """
        To push a message in the Notification Queue
        Params:
            - message: message dict that is to be passed as the message body
        """
        sqs.send_message(
            QueueUrl=os.environ["NOTIFICATION_QUEUE_URL"], MessageBody=json.dumps(message)
        )

@app.post("/order/create")
def add_orders():
    # Get the table name from the environment variable
    table_name = os.environ["TABLE_NAME"]

    # Parse the input JSON payload
    request_body = json.loads(app.current_event.body)

    # Extract product details from the request
    product_id = request_body.get("productId")
    order_address = request_body.get("orderAddress")

    # Check if required fields are provided
    if not product_id or not order_address:
        return {
            "statusCode": 400,
            "body": "productId and orderAddress are required fields.",
        }

    # Generate a unique product ID (you can use a more sophisticated method)
    order_id = str(hash(str(product_id) + order_address))

    # Create a new product item in DynamoDB
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "orderId": {"S": order_id},
            "productId": {"N": str(product_id)},
            "orderAddress": {"S": order_address},
            "orderPaymentStatus": {"BOOL": False},
        },
    )

    push_message_on_notification_queue(
        {
            "event": "order_created",
            "orderId": order_id,
            "orderAddress": order_address,
            "productId": product_id
        }
    )

    return "Successfully Created"



@app.get("/order/list")
def get_orders():
    try:
        # Get the table name from the environment variable
        table_name = os.environ["TABLE_NAME"]

        # Scan the DynamoDB table to fetch all entries
        response = dynamodb.scan(TableName=table_name)

        # Extract the items from the response
        items = response.get("Items", [])

        # Convert the items to a list of dictionaries
        orders = convert_dynamodb_json_to_readable(items)

        return orders
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}


def lambda_handler(event, context):
    return app.resolve(event, context)
