import json


def lambda_handler(event: dict, context:dict):
    # This is a SQS Message
    # Read the message body and decode the notification that we need to send
    sqs_message = event["Records"][0]
    sqs_body = json.loads(sqs_message["body"])

    if sqs_body["event"] == "order_created":

        # Send Email notification
        print(f"`Order-{sqs_body.get('orderId')} Received` Notification Sent Successfully")

    return "Success"
