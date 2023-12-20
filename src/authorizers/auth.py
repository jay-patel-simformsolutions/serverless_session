import json

def lambda_handler(event, context):
    # Extract headers from the API Gateway event
    headers = event.get('headers', {})

    # Check if a specific header is present
    required_header = 'Allow-me'
    if required_header in headers:
        # Allow the request by returning an IAM policy
        policy = generate_policy('user', 'Allow', event['methodArn'])
    else:
        # Deny the request by returning an IAM policy
        policy = generate_policy('user', 'Deny', event['methodArn'])
    print('!!!!!!!', policy)
    return policy

def generate_policy(principal_id, effect, resource):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        }
    }
    return policy
