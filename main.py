from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
from database import send_to_db

load_dotenv()
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

app = FastAPI(title="نظام اتحاد طلبة كلية الزراعة")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# أضف هذا الجزء فوراً
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح لأي مصدر
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ComplaintModel(BaseModel):
    name: str = "مجهول"
    subject: str
    message: str

@app.post("/api/complaints")
def receive_complaint(complaint: ComplaintModel):
    data = {"student_name": complaint.name, "subject": complaint.subject, "message": complaint.message, "status": "قيد المراجعة"}
    return send_to_db("complaints", data)

@app.get("/api/all-complaints")
def get_all_complaints():
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    url = f"{URL}/rest/v1/complaints?select=*"
    with httpx.Client() as client:
        return client.get(url, headers=headers).json()

@app.post("/api/reply/{complaint_id}")
def reply_to_complaint(complaint_id: int, reply_data: dict):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}
    url = f"{URL}/rest/v1/complaints?id=eq.{complaint_id}"
    data = {"admin_reply": reply_data["reply"], "status": "تم الرد"}
    with httpx.Client() as client:
        return client.patch(url, json=data, headers=headers).json()