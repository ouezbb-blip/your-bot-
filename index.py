from flask import Flask, request
import os
import json
import requests
import logging

app = Flask(__name__)

# === إعدادات ===
BOT_TOKEN = "8860089713:AAGFDiNlsmlTzk4LK8BxTpta1EsL6zgWPhA"
ADMIN_ID = "8553407440"
YOUR_BINANCE_ID = "1025308119"   # غيّرها

DATA_DIR = "/tmp/@wolf_data"     # مهم: استخدم /tmp على Vercel

WEBHOOK_PATH = "/webhook"

TG = f"https://api.telegram.org/bot{BOT_TOKEN}"

# إنشاء المجلدات
os.makedirs(DATA_DIR, exist_ok=True)

# باقي الدوال (read_list, write_item, is_vip ... ) نفسها السابقة
# (انسخها من الكود السابق)

def read_list(name):
    path = os.path.join(DATA_DIR, f"{name}.txt")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [x.strip() for x in f.readlines() if x.strip()]

def write_item(name, item):
    item = str(item)
    path = os.path.join(DATA_DIR, f"{name}.txt")
    items = read_list(name)
    if item not in items:
        with open(path, "a", encoding="utf-8") as f:
            f.write(item + "\n")

def is_vip(uid):
    return str(uid) in read_list("vip")

# ... (انسخ باقي الدوال: send, answer_cb, handle_update ...)

@app.route("/", methods=["GET"])
def home():
    return "✅ Wolf Bot is Running on Vercel!"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        handle_update(update)
    return "ok", 200

# يجب أن يكون app موجود في آخر الملف
