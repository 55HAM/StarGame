# HAM-FH — ملاحظات النشر

## المنصة
Render (الخطة المجانية).

## الرابط
https://ham-fh.onrender.com  ← سيُحدَّث عند تغيير الاسم لاحقًا

## ملفات النشر
- `render.yaml` في جذر المشروع: تكوين Render.
- `deploy/requirements.txt`: مكتبات Python المطلوبة.
- `deploy/NOTES.md` (هذا الملف).

## كيف يُنشر التحديث
من داخل Termux في مجلد المشروع:
    git add .
    git commit -m "وصف التعديل"
    git push

Render سيكتشف التغيير ويعيد النشر تلقائيًا خلال دقيقتين.

## الخطة المجانية — قيود يجب معرفتها
- الخدمة تنام بعد 15 دقيقة من عدم وجود زيارات.
- عند أول زيارة بعد النوم، يأخذ الاستيقاظ 30–60 ثانية.
- الحل لاحقًا: UptimeRobot لعمل ping كل 5 دقائق.

## عند تغيير الاسم لاحقًا
عدّل `name:` في `render.yaml`، ثم:
    git add render.yaml
    git commit -m "Rename service"
    git push
Render سيغيّر النطاق تلقائيًا.

## للعودة للمشروع بعد انقطاع طويل
1. افتح المستودع على GitHub واقرأ `readme.txt` و `deploy/NOTES.md`.
2. ادخل Render، تحقق من آخر نشر ناجح.
3. أي تعديل جديد: اتبع خطوات git أعلاه.



cd "/storage/emulated/0/HAM/Projects/# online/HAM-FH"
pkg install git -y
git config --global user.name "اسمك"
git config --global user.email "بريدك@example.com"