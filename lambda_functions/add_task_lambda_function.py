# lambda_function.py  —— ADD_TASK
import json
import os
import boto3
from uuid import uuid4
from datetime import datetime

# Initialize DynamoDB 
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TASK_TABLE_NAME", "Task_Table")  # 或者你在 Lambda 环境变量里写死 Table 名
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        
        body = json.loads(event.get("body", "{}"))
        content  = body["Content"]    # 前端约定字段名
        due_date = body["Due_Date"]   # 前端约定字段名

        # create item
        item = {
            "Task_ID":   str(uuid4()),
            "Content":   content,
            "Due_Date":  due_date,
            "Status":    "pending",
            "Timestamp": datetime.utcnow().isoformat()
        }

        # write to DynamoDB
        table.put_item(Item=item)

        
        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }



