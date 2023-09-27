build:
	sam build

deploy:
	sam deploy --stack-name $(STACK_NAME) --resolve-s3 --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM CAPABILITY_NAMED_IAM --region us-east-1

start:
	sam local start-api