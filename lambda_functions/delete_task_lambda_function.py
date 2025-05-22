# delete_task.py

import json
import os
import boto3


dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TASK_TABLE_NAME", "Task_Table")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        raw_body = event.get("body")
        if raw_body:
            payload = json.loads(raw_body)
        else:
            payload = event

        task_id = (
            payload.get("Task_ID")
            or payload.get("task_id")
            or payload.get("id")
        )
        if not task_id:
            raise ValueError("Missing Task_ID in payload")


        table.delete_item(Key={"Task_ID": task_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"deleted": task_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


