import os
import boto3

#creating dynamdbclient
dynamodb = boto3.client("dynamodb")
TableName = "budgeting_app_db"



def insert_period(period, income, expenses, comment):
    response = dynamodb.put_item(
        TableName=TableName,
        Item={
            'period': {'S': period},
            'income': {'N': income},
            'expenses': {'N': expenses},
            'comment': {'S': comment}
        }
    )
    return response



#fetchdata from table
def fetch_all_periods():
    response = dynamodb.scan(
        TableName=TableName,
        ProjectionExpression='period'
    )
    periods = [item['period'] for item in response['Items']]
    return periods

#get actual period
def get_period(period):
    response = dynamodb.get_item(
        TableName=TableName,
        Key={
            'period': {'S': period}
        }
    )
    item = response['Item']
    return item

period = "jun_2021"
income = 6000
expenses = 4500
comment = "null"

insert_period(period = period, income= income, expenses = expenses, comment= comment)