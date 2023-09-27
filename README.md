# serverless_session

### Basic template to build and deploy serverless Application using AWS SAM. It uses `aws-lambda-powertools` to develop API and dynamoDB as a Database

# Make commands

- `make build` : Build the deployment package for the AWS SAM cli
- `make deploy STACK_NAME=<stack-name>` : deploy the built package using AWS SAM cli
- `make start` : Start a server in your local machine based on the specified SAM template. You would need Docker running for this. It replicates the AWS API Gateway, AWS Lambda, etc envs in your local machine using Docker images
