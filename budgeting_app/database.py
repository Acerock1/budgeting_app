import os
import boto3

dynamodb = boto3.client("dynamodb")
TableName = "budgeting_app_db"



def insert_period(period, income, expenses, comment):
    dynamodb.put_item(
        TableName = TableName,
        Item={
            'period': {'S': period},
            'income': {'N': income},
            'expenses': {'N': expenses},
            'comment': {'S': comment}
        }
    )




def fetch_all_periods():
    response = dynamodb.scan(
        TableName=TableName,
        ProjectionExpression='period'
    )
    periods = [item['period'] for item in response['Items']]
    return periods


def get_period(period):
    response = dynamodb.get_item(
        TableName=TableName,
        Key={
            'period': {'S': period}
        }
    )
    item = response['Item']
    return item
