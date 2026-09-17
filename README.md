# IraqJobs V2

تطبيق وظائف عراقي مبني بـ Expo + React Native + Supabase.

## التشغيل

1. ثبّت Node.js.
2. افتح مجلد المشروع.
3. نفّذ:
   npm install
4. انسخ `.env.example` إلى `.env`.
5. ضع بيانات مشروع Supabase داخل `.env`.
6. افتح Supabase > SQL Editor والصق محتوى `supabase/schema.sql` وشغّله.
7. شغّل:
   npx expo start

## مهم

لا تضع `service_role` key داخل تطبيق Expo. استخدم فقط `anon/publishable key` في التطبيق، واترك الصلاحيات لسياسات RLS.

## GitHub

ارفع كل الملفات كما هي إلى المستودع، لكن لا ترفع `.env`.
