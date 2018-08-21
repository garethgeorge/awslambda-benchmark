import argparse 
import json 
import boto3
import sys, os
from botocore import UNSIGNED
from botocore.config import Config

parser = argparse.ArgumentParser(description='Run a benchmark')
parser.add_argument('mode', help='are we using the AWS endpoint or localhost?')
args = parser.parse_args()

if args.mode.lower() == "localhost": 
    print("LOCALHOST MODE")
    awslambda = boto3.client('lambda', 
        config=Config(signature_version=UNSIGNED),
        endpoint_url="http://localhost:80"
    )

elif args.mode.lower() == "aws":

    print("AWS MODE")
    with open('aws.json', 'r') as f:
        aws_creds = json.load(f)
    
    awslambda = boto3.client('lambda', 
        aws_access_key_id=aws_creds["aws_access_key_id"],
        aws_secret_access_key=aws_creds["aws_secret_access_key"],
    )

else:

    print("Invalid mode was specified.")
    sys.exit(1)


payload = b"""{
  "a": 15,
  "b": 22
}"""

for x in range(0, 100):
    print("trying to call...")
    response = awslambda.invoke(
        FunctionName="add",
        InvocationType='RequestResponse',
        Payload=payload
    )  
    print(response)
    print(response["Payload"].read())