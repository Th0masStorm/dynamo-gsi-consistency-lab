#!/usr/bin/env python3
from botocore.exceptions import ClientError
from datetime import datetime as dt
import multiprocessing
import uuid
import boto3 # pip install boto3


STACK_NAME = 'dynamo'
INDEX_NAME = 'GSI'


def get_table_name() -> str:
    cfn = boto3.client('cloudformation')
    try:
        return cfn.describe_stacks(StackName=STACK_NAME)['Stacks'][0]['Outputs'][0]['OutputValue']
    except KeyError:
        raise ValueError('Could not retrieve table name!')


def generate_item() -> dict:
    return {
        'PartitionKey': {'S': str(uuid.uuid4())},
        'SortKey': {'S': str(uuid.uuid4())},
        'GSIKey': {'S': str(uuid.uuid4())},
    }

def process_items() -> None:
    table_name = get_table_name()
    dynamo = boto3.client('dynamodb')
    while True:
        item = generate_item()
        gsi_key = item['GSIKey']['S']

        try:
            dynamo.put_item(TableName=table_name, Item=item)
        except ClientError as error:
            if error.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                print('Oh noes, I throttled during write!')
            else:
                print(error)

        try:
            counts = 1
            while True:
                start = dt.now()
                r = dynamo.query(TableName=table_name,
                                IndexName=INDEX_NAME,
                                KeyConditionExpression = f'GSIKey = :gsi_key',
                                ExpressionAttributeValues={':gsi_key':{'S': gsi_key}})
                if r['Count'] == 0:
                    counts += 1
                else:
                    if counts > 1:
                        end = dt.now()
                        delta = (end - start)

                        print(f'Got item {gsi_key} from the {counts} attempt. Took {delta.total_seconds() * 1000} ms')
                    break

        except ClientError as error:
            if error.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                print('Oh noes, I throttled during Query!')
            else:
                print(error)

def main():
    processes = []
    processors = multiprocessing.cpu_count()

    for _ in range(processors):
        p = multiprocessing.Process(target=process_items)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main()