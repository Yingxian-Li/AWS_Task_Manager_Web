# update_task_status.py

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

        task_id    = payload.get("Task_ID")    or payload.get("task_id")    or payload.get("id")
        new_status = payload.get("Status")     or payload.get("status")     or payload.get("new_status")

        if not task_id or not new_status:
            raise ValueError("Missing Task_ID or Status in payload")


        result = table.update_item(
            Key={"Task_ID": task_id},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "Status"},
            ExpressionAttributeValues={":s": new_status},
            ReturnValues="UPDATED_NEW"       
        )


        return {
            "statusCode": 200,
            "body": json.dumps({
                "Task_ID": task_id,
                "updated": result["Attributes"]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
