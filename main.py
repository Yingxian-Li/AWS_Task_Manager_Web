# main.py

import os
import json

import boto3
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# ===== 1. Load AWS credentials from .env =====
load_dotenv()
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION            = os.getenv("AWS_REGION", "us-east-1")

# ===== 2. Lambda function names =====
ADD_FN    = "add_task"
GET_FN    = "get_task"
UPDATE_FN = "update_task_status"
DELETE_FN = "delete_task"

# ===== 3. Initialize Lambda client =====
lambda_client = boto3.client(
    "lambda",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def invoke_lambda(fn_name: str, payload: dict) -> dict:
    """Invoke a Lambda and parse the JSON response."""
    resp = lambda_client.invoke(
        FunctionName=fn_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    text = resp["Payload"].read().decode("utf-8")
    return json.loads(text)

# ===== 4. Streamlit UI =====
st.set_page_config(page_title="Task Manager", page_icon="📝")
st.title("📝 Task Manager with AWS Lambda")


with st.expander("➕ Add a New Task", expanded=True):
    content  = st.text_input("✏️ Task Content")
    due_date = st.date_input("📅 Due Date", value=datetime.utcnow().date())
    if st.button("➕ Add Task"):
        if not content.strip():
            st.error("Task Content 不能为空")
        else:
            payload = {
                "body": json.dumps({
                    "Content":   content,
                    "Due_Date":  due_date.strftime("%Y-%m-%d"),
                })
            }
            res = invoke_lambda(ADD_FN, payload)
            if res.get("statusCode") == 200:
                st.success("✅ Task added!")
            else:
                st.error(f"Add failed: {res}")

st.markdown("---")


if st.button("🔄 Refresh Task List"):  
    pass

st.subheader("📂 Current Tasks")


try:
    res = invoke_lambda(GET_FN, {"body": "{}"})
    if res.get("statusCode") != 200:
        st.error(f"Error querying tasks: {res}")
    else:
        tasks = json.loads(res.get("body", "[]"))
        if not tasks:
            st.info("No tasks yet.")
        for task in tasks:
            tid     = task.get("Task_ID", "")
            content = task.get("Content", "")
            due     = task.get("Due_Date", "")
            status  = task.get("Status", "")

            st.markdown(f"**{content}** — Due: `{due}` — Status: `{status}`")
            c1, c2 = st.columns([1,1])
            with c1:
                if status != "finished" and st.button("✅ Complete", key=f"up_{tid}"):
                    upd_payload = {
                        "body": json.dumps({
                            "Task_ID":    tid,
                            "new_status": "finished"
                        })
                    }
                    r2 = invoke_lambda(UPDATE_FN, upd_payload)
                    if r2.get("statusCode") == 200:
                        st.success("✔️ Marked as finished")
                    else:
                        st.error(f"Update failed: {r2}")
            with c2:
                if st.button("❌ Delete", key=f"del_{tid}"):
                    del_payload = {"body": json.dumps({"Task_ID": tid})}
                    r3 = invoke_lambda(DELETE_FN, del_payload)
                    if r3.get("statusCode") == 200:
                        st.success("🗑️ Deleted")
                    else:
                        st.error(f"Delete failed: {r3}")

except Exception as e:
    st.error(f"Frontend error occurred: {e}")













