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
- `lambda/` - Folder with Lambda function files (e.g., `add_task`, `update_task_status`, etc.)

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
