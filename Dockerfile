# استخدام صورة Python خفيفة
FROM python:3.11-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المتطلبات أولاً للاستفادة من التخزين المؤقت
COPY deploy/requirements.txt .

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تعريض المنفذ الذي سيعمل عليه الخادم
EXPOSE 8000

# أمر تشغيل الخادم (يستخدم المنفذ 8000 داخليًا)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]