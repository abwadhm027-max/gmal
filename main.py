from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock

class JobPortalApp(App):
    def build(self):
        self.user_email = "غير مرتبط"
        # قاعدة بيانات مؤقتة لتخزين الوظائف المنشورة
        self.jobs_database = [
            {"type": "كهربائي - المحاويل", "wage": "35,000 د.ع", "time": "صباحي", "phone": "07801234567", "status": "متاح"}
        ]
        
        # التخطيط الرئيسي للتطبيق متمركز باحترافية
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, 
                           size_hint=(0.95, None), height=560,
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # عنوان التطبيق الرئيسي
        title_label = Label(text='منصة سوق العمل', font_size=22, size_hint_y=None, height=40, color=(0.9, 0.9, 1, 1))
        layout.add_widget(title_label)
        
        # مساحة عرض الحالة والأخبار
        self.status_label = Label(text='الرجاء ربط حساب الجيميل للبدء', font_size=13, size_hint_y=None, height=110, color=(0.8, 0.8, 0.8, 1))
        layout.add_widget(self.status_label)
        
        # زر استعراض الأعمال المتوفرة
        btn_jobs = Button(text='الأعمال المتوفرة', font_size=15, size_hint_y=None, height=45, background_color=(0.1, 0.5, 0.3, 1))
        btn_jobs.bind(on_press=self.on_jobs_click)
        layout.add_widget(btn_jobs)
        
        # زر نشر وظيفة (خاص بصاحب العمل)
        btn_post = Button(text='نشر وظيفة (صاحب العمل)', font_size=15, size_hint_y=None, height=45, background_color=(0.8, 0.4, 0.1, 1))
        btn_post.bind(on_press=self.on_post_job_click)
        layout.add_widget(btn_post)
        
        # زر تقديم الطلب والاتصال والدردشة
        btn_apply = Button(text='تقديم الطلب والاتصال', font_size=15, size_hint_y=None, height=45, background_color=(0.2, 0.4, 0.8, 1))
        btn_apply.bind(on_press=self.on_apply_click)
        layout.add_widget(btn_apply)
        
        # زر حسابي الشخصي
        btn_account = Button(text='حسابي الشخصي', font_size=15, size_hint_y=None, height=45, background_color=(0.5, 0.2, 0.6, 1))
        btn_account.bind(on_press=self.on_account_click)
        layout.add_widget(btn_account)
        
        # زر تحديد الموقع الجغرافي GPS
        btn_location = Button(text='تحديد الموقع (GPS)', font_size=15, size_hint_y=None, height=45, background_color=(0.3, 0.3, 0.3, 1))
        btn_location.bind(on_press=self.on_location_click)
        layout.add_widget(btn_location)
        
        # إظهار نافذة تسجيل الدخول تلقائياً عند الإقلاع
        Clock.schedule_once(self.show_login_popup, 0.4)
        
        return layout

    def show_login_popup(self, dt):
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content.add_widget(Label(text='الرجاء ربط حساب الجيميل للمتابعة:', font_size=13, size_hint_y=None, height=30))
        
        self.email_input = TextInput(hint_text='example@gmail.com', multiline=False, size_hint_y=None, height=40)
        content.add_widget(self.email_input)
        
        login_btn = Button(text='ربط الحساب', font_size=15, size_hint_y=None, height=42, background_color=(0.1, 0.5, 0.3, 1))
        
        popup = Popup(title='تسجيل الدخول', content=content, size_hint=(0.85, 0.4), auto_dismiss=False)
        login_btn.bind(on_press=lambda x: self.save_email(popup))
        content.add_widget(login_btn)
        
        popup.open()

    def save_email(self, popup):
        email = self.email_input.text.strip()
        if "@gmail.com" in email:
            self.user_email = email
            self.status_label.text = f"تم الربط بنجاح: {self.user_email}\nالموقع: المحاويل، بابل"
            popup.dismiss()
        else:
            self.email_input.hint_text = "خطأ! ادخل بريد جيميل صحيح"
            self.email_input.text = ""

    def on_jobs_click(self, instance):
        if self.user_email == "غير مرتبط":
            self.status_label.text = "خطأ: الرجاء ربط الجيميل أولاً!"
            self.show_login_popup(0)
            return
            
        feed_text = "--- قائمة الأعمال المتوفرة ---\n"
        for i, job in enumerate(self.jobs_database, 1):
            feed_text += f"{i}. {job['type']} | الأجرة: {job['wage']}\n   الوقت: {job['time']} | الحالة: [{job['status']}]\n"
        self.status_label.text = feed_text

    def on_post_job_click(self, instance):
        if self.user_email == "غير مرتبط":
            self.status_label.text = "خطأ: الرجاء ربط الجيميل أولاً!"
            self.show_login_popup(0)
            return
            
        # استمارة صاحب العمل لنشر الوظيفة
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        content.add_widget(Label(text='نوع العمل (مثال: بناء، كهربائي):', font_size=12, size_hint_y=None, height=25))
        self.job_type_input = TextInput(hint_text='عنوان العمل...', multiline=False, size_hint_y=None, height=35)
        content.add_widget(self.job_type_input)
        
        content.add_widget(Label(text='اليومية (مثال: 35 ألف):', font_size=12, size_hint_y=None, height=25))
        self.wage_input = TextInput(hint_text='المبلغ...', multiline=False, size_hint_y=None, height=35)
        content.add_widget(self.wage_input)
        
        content.add_widget(Label(text='الوقت / ساعات العمل:', font_size=12, size_hint_y=None, height=25))
        self.time_input = TextInput(hint_text='ساعات العمل...', multiline=False, size_hint_y=None, height=35)
        content.add_widget(self.time_input)
        
        content.add_widget(Label(text='رقم هاتف صاحب العمل:', font_size=12, size_hint_y=None, height=25))
        self.phone_input = TextInput(hint_text='رقم الهاتف...', multiline=False, size_hint_y=None, height=35)
        content.add_widget(self.phone_input)
        
        post_btn = Button(text='نشر في الواجهة الرئيسية', font_size=14, size_hint_y=None, height=40, background_color=(0.8, 0.4, 0.1, 1))
        
        popup = Popup(title='إضافة وظيفة جديدة', content=content, size_hint=(0.9, 0.8))
        post_btn.bind(on_press=lambda x: self.save_new_job(popup))
        content.add_widget(post_btn)
        
        popup.open()

    def save_new_job(self, popup):
        j_type = self.job_type_input.text.strip()
        j_wage = self.wage_input.text.strip()
        j_time = self.time_input.text.strip()
        j_phone = self.phone_input.text.strip()
        
        if j_type and j_wage and j_time and j_phone:
            new_job = {
                "type": j_type, 
                "wage": j_wage, 
                "time": j_time, 
                "phone": j_phone, 
                "status": "متاح"
            }
            self.jobs_database.append(new_job)
            self.status_label.text = f"تم نشر الوظيفة بنجاح: {j_type}\nاضغط على 'الأعمال المتوفرة' لمشاهدتها."
            popup.dismiss()
        else:
            self.status_label.text = "خطأ: يرجى ملء كافة الحقول لنشر الوظيفة."

    def on_apply_click(self, instance):
        if self.user_email == "غير مرتبط":
            self.status_label.text = "خطأ: الرجاء ربط الجيميل أولاً!"
            self.show_login_popup(0)
            return
            
        # نافذة تواصل العامل وتحديث الحالة إلى "تم العمل"
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content.add_widget(Label(text='أدخل رقم العمل للقبول والدردشة:', font_size=13, size_hint_y=None, height=30))
        
        self.job_num_input = TextInput(hint_text='مثال: 1', multiline=False, size_hint_y=None, height=40)
        content.add_widget(self.job_num_input)
        
        content.add_widget(Label(text='رسالة إلى صاحب العمل:', font_size=13, size_hint_y=None, height=30))
        self.msg_input = TextInput(hint_text='أنا جاهز لهذا العمل...', multiline=False, size_hint_y=None, height=40)
        content.add_widget(self.msg_input)
        
        chat_btn = Button(text='إرسال وتغيير الحالة إلى (تم العمل)', font_size=14, size_hint_y=None, height=45, background_color=(0.2, 0.4, 0.8, 1))
        
        popup = Popup(title='التواصل وتأكيد العمل', content=content, size_hint=(0.85, 0.7))
        chat_btn.bind(on_press=lambda x: self.process_agreement(popup))
        content.add_widget(chat_btn)
        
        popup.open()

    def process_agreement(self, popup):
        try:
            index = int(self.job_num_input.text.strip()) - 1
            msg = self.msg_input.text.strip()
            if 0 <= index < len(self.jobs_database):
                # تحويل حالة الوظيفة إلى مكتملة / تم العمل
                self.jobs_database[index]['status'] = "تم العمل (مكتمل)"
                target_phone = self.jobs_database[index]['phone']
                self.status_label.text = f"تم إرسال الرسالة لصاحب العمل ({target_phone})!\nالرسالة: {msg}\nالحالة: تم تحديث الوظيفة إلى [تم العمل]."
                popup.dismiss()
            else:
                self.status_label.text = "خطأ: رقم العمل غير صحيح."
        except ValueError:
            self.status_label.text = "خطأ: يرجى إدخال رقم صحيح للعمل."

    def on_account_click(self, instance):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        content.add_widget(Label(text=f'ملف الحساب الشخصي\n\nالبريد: {self.user_email}\nالموقع: المحاويل، بابل، العراق', font_size=14))
        
        close_btn = Button(text='إغلاق', size_hint_y=None, height=42, background_color=(0.5, 0.2, 0.6, 1))
        popup = Popup(title='حسابي', content=content, size_hint=(0.8, 0.45))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def on_location_click(self, instance):
        if self.user_email == "غير مرتبط":
            self.status_label.text = "خطأ: الرجاء ربط الجيميل أولاً!"
            self.show_login_popup(0)
        else:
            self.status_label.text = f"GPS فعال | الحساب: {self.user_email}\nالموقع الحالي: المحاويل، بابل، العراق"

if __name__ == '__main__':
    JobPortalApp().run()
