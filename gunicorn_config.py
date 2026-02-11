import multiprocessing
import os

# عدد العمال: نستخدم صيغة (2 * عدد الأنوية + 1) لضمان أقصى أداء
workers = multiprocessing.cpu_count() * 2 + 1

# نوع العمال: 'gevent' أو 'sync' - نختار sync حالياً لاستقرار البوت
worker_class = 'sync'

# المهلة الزمنية: رفعناها لـ 120 ثانية لضمان عدم انقطاع سحب الملفات الكبيرة
timeout = 120

# الارتباط: المنفذ الذي سيفتح عليه السيرفر
bind = "0.0.0.0:" + os.environ.get("PORT", "5000")

# تسجيل الوصول: لتتبع كل حركة دخول للموقع (مهم لتحليل تدفق البيانات)
accesslog = "-"
errorlog = "-"
