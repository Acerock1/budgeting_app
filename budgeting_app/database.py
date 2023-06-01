import os
import boto3

#creating dynamdbclient
dynamodb = boto3.client("dynamodb")
TableName = "budgeting_app_db"


#write to table
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


insert_period(period = {"S","jun_2022"}, income = {"N", 6000}, expenses = {"N", 4500}, comment = {"S", "null"})