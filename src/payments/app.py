from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import os
import json
import boto3
from utils import convert_dynamodb_json_to_readable

# Initialize the DynamoDB client
dynamodb = boto3.client("dynamodb")
event_bridge = boto3.client("events")

app = APIGatewayRestResolver()


@app.post("/payment/pay")
def pay():
    # Get the table name from the environment variable
    table_name = os.environ["TABLE_NAME"]

    # Parse the input JSON payload
    request_body = json.loads(app.current_event.body)

    # Extract payments details from the request
    order_id = request_body.get("orderId")
    transaction_amount = request_body.get("transactionAmount")

    # Check if required fields are provided
    if not order_id or not transaction_amount:
        return {
            "statusCode": 400,
            "body": "orderId and transactionAmount are required fields.",
        }

    # TODO: DO stripe payment and only on success proceed from here

    # Generate a unique payment ID
    payment_id = str(hash(str(order_id)))

    # Create a new payment item in DynamoDB
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "paymentId": {"S": str(payment_id)},
            "orderId": {"S": str(order_id)},
            "transactionAmount": {"S": transaction_amount},
        },
    )

    # Publish an event
    event_bridge.put_events(
        Entries=[
            {
                "Source": "payments-service",
                "DetailType": "payment-success",
                "Detail": json.dumps(
                    {
                        "paymentId": payment_id,
                        "orderId": order_id,
                        "transaction_amount": transaction_amount,
                    }
                ),
                "EventBusName": os.environ["EVENT_BUS_NAME"],
            },
        ],
    )

    return "Payment Received"


def lambda_handler(event, context):
    return app.resolve(event, context)
