import boto3

def sign_in(username, password, user_pool_id, client_id):
    client = boto3.client('cognito-idp')

    auth_params = {
        'USERNAME': username,
        'PASSWORD': password,
    }

    try:
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters=auth_params
        )

        print("Authentication successful")
        print("Access Token:", response['AuthenticationResult']['IdToken'])

    except client.exceptions.NotAuthorizedException as e:
        print("Authentication failed:", e)
    except client.exceptions.UserNotFoundException as e:
        print("User not found:", e)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    # Replace these values with your own
    username = 'jay.patel@simformsolutions.com'
    password = 'Test@123'
    user_pool_id = 'us-east-1_3bFeYNBXW'
    client_id = '61iiktcprq40a3iqmjdirk4082'

    sign_in(username, password, user_pool_id, client_id)
