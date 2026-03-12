import httpx
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

# دالة لإرسال البيانات مباشرة لقاعدة البيانات
def send_to_db(table, data):
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    url = f"{URL}/rest/v1/{table}"
    
    with httpx.Client() as client:
        response = client.post(url, json=data, headers=headers)
        return response.json()