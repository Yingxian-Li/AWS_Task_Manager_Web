# AWS Lambda Task Manager 📝

This project is a simple task manager web app built using **Streamlit**, **AWS Lambda**, and **DynamoDB**. Users can add, view, complete, and delete tasks via a web interface.

---

## ✨ Features

- ✅ Add new tasks with due date
- 📂 View all current tasks
- 🟩 Mark tasks as **finished**
- ❌ Delete tasks
- ☁️ All data stored in **DynamoDB**
- 🔁 Business logic handled via **AWS Lambda**

---

## 📁 Project Structure

- `main.py` - Streamlit frontend
- `.env` - Local environment file with AWS keys (not committed)
- `lambda/` - Folder with Lambda function files
   - add_task_lambda_function.py
   - delete_task_lambda_function.py
   - get_task_lambda_function.py
   - update_task_lambda_function.py

---

## 🔐 .env Configuration

Make sure your `.env` file includes:

```env
AWS_ACCESS_KEY_ID=your_key_id
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

---

## 🚀 How to Run

1. **Install dependencies**:
   ```bash
   pip install streamlit python-dotenv boto3
2. **Navigate to the project directory (adjust the path if needed)**:
   ```bash
   cd ~/path/AWS_Web_TaskManager
3. **Run the Streamlit app**:
   ```bash
   streamlit run main.py
4. **Verify that your AWS credentials in .env are valid and have permissions for Lambda and DynamoDB**.
5. **Open in browser: The app should automatically open at http://localhost:8501**.

---

📌 Notes
- You must have an AWS account with an IAM user or role that has permissions for:

    -lambda:InvokeFunction

    -dynamodb:GetItem, dynamodb:PutItem, dynamodb:UpdateItem, etc.
- Make sure your Lambda functions are already deployed and publicly callable (or exposed via API Gateway, if needed).