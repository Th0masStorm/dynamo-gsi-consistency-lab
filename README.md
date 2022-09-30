# DynamoDB GSI eventual consistency lab

This lab is built to measure the consistency strength on GSI.

## A word of warning
DynamoDB tables are not free, this lab uses OnDemand billing model.

## Getting started
You will need some AWS skills, boto3

## Running a lab
1. Create a DynamoDB table: `aws cloudformation deploy --stack-name dynamo --template-file template.yml`
2. Run the load simulator, logging to the file: `./dynamo.py > out.log`
3. Keep the simulator running for a while.
4. When bored or done, cancel the execution with CTRL-C
5. Get total items: `./percentile.sh`
6. Clean up: `aws cloudformation delete-stack --stack-name dynamo`

# To Do
- [ ] Rewrite it in Go, Rust, Java, pure C or whatever allows very fast parallel code execution
- [ ] Bring Your Own Item Generator
- [ ] Support provisioned CUs
