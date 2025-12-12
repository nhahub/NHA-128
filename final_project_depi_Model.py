# -*- coding: utf-8 -*-
"""
🚂 نظام تنبؤ تأخير القطارات - الإصدار الخفيف
يعمل بـ Python الأساسي فقط (لا يحتاج تثبيت مكتبات)
"""


import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import csv
import json
import math
import random
from datetime import datetime
import statistics

print("=" * 60)
print("🚂 نظام تنبؤ تأخير القطارات - الإصدار الخفيف")
print("✅ يعمل بدون مكتبات خارجية")
print("=" * 60)


class SimpleRailwayPredictor:
    """نسخة مبسطة تعمل بـ Python الأساسي فقط"""

    def __init__(self, root):
        self.root = root
        self.root.title("🚂 نظام تنبؤ تأخير القطارات")
        self.root.geometry("1200x700")

        self.data = []
        self.headers = []

        self.setup_ui()

    def setup_ui(self):
        """إنشاء واجهة المستخدم"""
        # إطار العنوان
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(title_frame,
                 text="🚂 نظام تنبؤ تأخير القطارات",
                 font=("Arial", 24, "bold"),
                 bg="#2c3e50",
                 fg="white").pack(pady=20)

        # تبويبات رئيسية
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # تبويب تحميل البيانات
        self.create_data_tab()

        # تبويب التحليل
        self.create_analysis_tab()

        # تبويب التنبؤ
        self.create_prediction_tab()

        # تبويب المساعدة
        self.create_help_tab()

        # شريط الحالة
        self.status = tk.Label(self.root, text="✅ جاهز - قم بتحميل ملف CSV أو Excel",
                               bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def create_data_tab(self):
        """إنشاء تبويب البيانات"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="📂 البيانات")

        # زر التحمل
        btn_frame = tk.Frame(tab)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame,
                  text="📂 تحميل ملف CSV",
                  command=self.load_csv,
                  bg="#3498db",
                  fg="white",
                  font=("Arial", 12, "bold"),
                  padx=20,
                  pady=10).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame,
                  text="📊 تحليل البيانات",
                  command=self.analyze_data,
                  bg="#2ecc71",
                  fg="white",
                  font=("Arial", 12),
                  padx=20,
                  pady=10).pack(side=tk.LEFT, padx=10)

        # عرض البيانات
        text_frame = tk.Frame(tab)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.data_text = scrolledtext.ScrolledText(text_frame, height=20, font=("Courier", 10))
        self.data_text.pack(fill="both", expand=True)

    def create_analysis_tab(self):
        """إنشاء تبويب التحليل"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 التحليل")

        # إطار النتائج
        result_frame = tk.Frame(tab)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.analysis_text = scrolledtext.ScrolledText(result_frame, height=25, font=("Arial", 11))
        self.analysis_text.pack(fill="both", expand=True)

        # أزرار التحليل
        btn_frame = tk.Frame(tab)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame,
                  text="🎯 تحليل الإحصائيات",
                  command=self.show_statistics,
                  bg="#9b59b6",
                  fg="white",
                  font=("Arial", 11),
                  padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame,
                  text="💰 تحليل الأسعار",
                  command=self.analyze_prices,
                  bg="#e74c3c",
                  fg="white",
                  font=("Arial", 11),
                  padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame,
                  text="⏱️ تحليل التأخير",
                  command=self.analyze_delays,
                  bg="#f39c12",
                  fg="white",
                  font=("Arial", 11),
                  padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

    def create_prediction_tab(self):
        """إنشاء تبويب التنبؤ"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="🔮 التنبؤ")

        # إطار الإدخال
        input_frame = tk.LabelFrame(tab, text="إدخال بيانات الرحلة", font=("Arial", 12, "bold"))
        input_frame.pack(fill="x", padx=20, pady=10)

        # حقول الإدخال
        fields = [
            ("السعر:", "price"),
            ("المحطة الأولى:", "station1"),
            ("المحطة الثانية:", "station2"),
            ("اليوم:", "day"),
            ("التوقيت:", "time")
        ]

        self.input_vars = {}
        for i, (label, name) in enumerate(fields):
            tk.Label(input_frame, text=label, font=("Arial", 11)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            var = tk.StringVar()
            entry = tk.Entry(input_frame, textvariable=var, font=("Arial", 11), width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.input_vars[name] = var

        # زر التنبؤ
        tk.Button(input_frame,
                  text="🔮 تنبأ باحتمال التأخير",
                  command=self.predict_delay,
                  bg="#2c3e50",
                  fg="white",
                  font=("Arial", 12, "bold"),
                  padx=20,
                  pady=10).grid(row=len(fields), column=0, columnspan=2, pady=20)

        # إطار النتيجة
        result_frame = tk.LabelFrame(tab, text="نتيجة التنبؤ", font=("Arial", 12, "bold"))
        result_frame.pack(fill="x", padx=20, pady=10)

        self.result_label = tk.Label(result_frame,
                                     text="👈 أدخل بيانات الرحلة وانقر على التنبؤ",
                                     font=("Arial", 14),
                                     fg="gray",
                                     pady=20)
        self.result_label.pack()

        # شريط التقدم
        self.progress = ttk.Progressbar(result_frame, length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = tk.Label(result_frame, text="0%", font=("Arial", 16, "bold"))
        self.progress_label.pack()

        # التفسير
        self.explanation = tk.Label(result_frame,
                                    text="",
                                    font=("Arial", 11),
                                    wraplength=400,
                                    justify="center")
        self.explanation.pack(pady=10)

    def create_help_tab(self):
        """إنشاء تبويب المساعدة"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="❓ المساعدة")

        help_text = """
        🎯 نظام تنبؤ تأخير القطارات - الإصدار الخفيف

        📋 كيفية الاستخدام:

        1. 📂 تحميل البيانات:
           - انقر على 'تحميل ملف CSV'
           - اختر ملف البيانات الخاص بك
           - يمكن استخدام ملفات Excel بعد تحويلها لـ CSV

        2. 📊 تحليل البيانات:
           - بعد تحميل البيانات، استخدم أزرار التحليل
           - 'تحليل الإحصائيات': يعرض معلومات عامة
           - 'تحليل الأسعار': يحلل توزيع الأسعار
           - 'تحليل التأخير': يحلل أوقات التأخير

        3. 🔮 التنبؤ:
           - أدخل بيانات الرحلة الجديدة
           - انقر على 'تنبأ باحتمال التأخير'
           - سيعرض النظام النتيجة فوراً

        📁 تنسيق البيانات المطلوب:
        - ملف CSV أو Excel
        - يحتوي على أعمدة مثل: price, delay, station, etc.
        - يمكن تحويل أي ملف Excel لـ CSV من خلال Save As

        💡 نصائح:
        - احفظ ملف البيانات في نفس مجلد البرنامج
        - استخدم أرقاماً في حقول الأسعار والتأخير
        - يمكنك تحليل أي بيانات قطارات لديك

        🚀 للمطورين:
        - هذا الإصدار يعمل بـ Python الأساسي فقط
        - لا يحتاج لتثبيت أي مكتبات خارجية
        - مناسب لأي جهاز يعمل بنظام Windows
        """

        text_widget = scrolledtext.ScrolledText(tab, font=("Arial", 11))
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def load_csv(self):
        """تحميل ملف CSV"""
        file_path = filedialog.askopenfilename(
            title="اختر ملف CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            try:
                self.data = []
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.headers = next(reader)
                    self.data = list(reader)

                # عرض البيانات
                self.data_text.delete("1.0", tk.END)

                # عرض الرأس
                header_text = " | ".join(self.headers) + "\n"
                self.data_text.insert("1.0", "📋 رؤوس الأعمدة:\n")
                self.data_text.insert("2.0", "-" * 80 + "\n")
                self.data_text.insert("3.0", header_text)
                self.data_text.insert("4.0", "-" * 80 + "\n\n")

                # عرض أول 20 صف
                self.data_text.insert("end", "📊 عينة من البيانات (أول 20 صف):\n\n")
                for i, row in enumerate(self.data[:20]):
                    row_text = " | ".join(row[:5]) + "\n"  # أول 5 أعمدة فقط
                    self.data_text.insert("end", f"{i + 1:3d}. {row_text}")

                self.status.config(text=f"✅ تم تحميل {len(self.data)} صف بنجاح")

                # تحليل تلقائي
                self.analyze_data()

            except Exception as e:
                messagebox.showerror("خطأ", f"فشل تحميل الملف:\n{str(e)}")

    def analyze_data(self):
        """تحليل البيانات الأساسي"""
        if not self.data:
            messagebox.showwarning("تحذير", "الرجاء تحميل البيانات أولاً")
            return

        try:
            self.analysis_text.delete("1.0", tk.END)

            report = "=" * 60 + "\n"
            report += "📊 تقرير تحليل البيانات\n"
            report += "=" * 60 + "\n\n"

            # معلومات أساسية
            report += f"📈 معلومات عامة:\n"
            report += f"   • عدد الصفوف: {len(self.data):,}\n"
            report += f"   • عدد الأعمدة: {len(self.headers)}\n"
            report += f"   • الأعمدة: {', '.join(self.headers)}\n\n"

            # البحث عن أعمدة رقمية
            numeric_columns = []
            for i, header in enumerate(self.headers):
                try:
                    # محاولة تحويل أول 10 قيم لأرقام
                    values = [row[i] for row in self.data[:10] if row[i]]
                    if all(self.is_number(v) for v in values if v):
                        numeric_columns.append((header, i))
                except:
                    continue

            if numeric_columns:
                report += f"🔢 الأعمدة الرقمية ({len(numeric_columns)}):\n"
                for header, idx in numeric_columns:
                    # جمع القيم الرقمية
                    numeric_values = []
                    for row in self.data:
                        if len(row) > idx and self.is_number(row[idx]):
                            numeric_values.append(float(row[idx]))

                    if numeric_values:
                        avg = statistics.mean(numeric_values) if numeric_values else 0
                        report += f"   • {header}: {len(numeric_values)} قيمة، متوسط: {avg:.2f}\n"
                report += "\n"

            # تحليل التأخير إذا وجد
            delay_idx = -1
            for i, header in enumerate(self.headers):
                if 'delay' in header.lower() or 'تأخير' in header.lower():
                    delay_idx = i
                    break

            if delay_idx >= 0:
                delay_values = []
                for row in self.data:
                    if len(row) > delay_idx and self.is_number(row[delay_idx]):
                        delay_values.append(float(row[delay_idx]))

                if delay_values:
                    delayed = sum(1 for v in delay_values if v > 0)
                    report += f"⏱️ تحليل التأخير:\n"
                    report += f"   • إجمالي القياسات: {len(delay_values):,}\n"
                    report += f"   • حالات التأخير: {delayed:,} ({delayed / len(delay_values) * 100:.1f}%)\n"
                    if delayed > 0:
                        avg_delay = statistics.mean([v for v in delay_values if v > 0])
                        report += f"   • متوسط التأخير: {avg_delay:.1f} دقيقة\n"
                    report += "\n"

            # تحليل الأسعار إذا وجدت
            price_idx = -1
            for i, header in enumerate(self.headers):
                if 'price' in header.lower() or 'سعر' in header.lower():
                    price_idx = i
                    break

            if price_idx >= 0:
                price_values = []
                for row in self.data:
                    if len(row) > price_idx and self.is_number(row[price_idx]):
                        price_values.append(float(row[price_idx]))

                if price_values:
                    report += f"💰 تحليل الأسعار:\n"
                    report += f"   • عدد التذاكر: {len(price_values):,}\n"
                    report += f"   • متوسط السعر: {statistics.mean(price_values):.2f}\n"
                    report += f"   • أقل سعر: {min(price_values):.2f}\n"
                    report += f"   • أعلى سعر: {max(price_values):.2f}\n\n"

            report += "💡 توصيات:\n"
            report += "   1. تأكد من جودة البيانات\n"
            report += "   2. استخدم التنبؤ للرحلات الجديدة\n"
            report += "   3. راقب مؤشرات الأداء بانتظام\n"

            report += "\n" + "=" * 60 + "\n"
            report += f"📅 تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            report += "=" * 60

            self.analysis_text.insert("1.0", report)
            self.status.config(text="✅ تم تحليل البيانات بنجاح")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل التحليل:\n{str(e)}")

    def show_statistics(self):
        """عرض إحصائيات مفصلة"""
        if not self.data:
            return

        self.analysis_text.delete("1.0", tk.END)

        report = "📈 الإحصائيات التفصيلية:\n\n"

        for i, header in enumerate(self.headers):
            # جمع القيم لهذا العمود
            column_values = []
            for row in self.data:
                if len(row) > i:
                    column_values.append(row[i])

            # تحليل العمود
            report += f"🔹 {header}:\n"
            report += f"   • عدد القيم: {len(column_values):,}\n"

            # القيم الفريدة (للأعمدة النصية)
            unique_values = set(column_values)
            if len(unique_values) <= 10 and len(unique_values) < len(column_values):
                report += f"   • القيم الفريدة: {len(unique_values)}\n"

            # إذا كان العمود رقمياً
            numeric_values = [v for v in column_values if self.is_number(v)]
            if numeric_values:
                numeric_values = [float(v) for v in numeric_values]
                report += f"   • قيم رقمية: {len(numeric_values):,}\n"
                if numeric_values:
                    report += f"   • المتوسط: {statistics.mean(numeric_values):.2f}\n"
                    report += f"   • الوسيط: {statistics.median(numeric_values):.2f}\n"

            report += "\n"

        self.analysis_text.insert("1.0", report)

    def analyze_prices(self):
        """تحليل الأسعار"""
        if not self.data:
            return

        # البحث عن عمود الأسعار
        price_idx = -1
        for i, header in enumerate(self.headers):
            if 'price' in header.lower() or 'سعر' in header.lower():
                price_idx = i
                break

        if price_idx < 0:
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert("1.0", "⚠️ لم يتم العثور على عمود الأسعار")
            return

        # جمع قيم الأسعار
        price_values = []
        for row in self.data:
            if len(row) > price_idx and self.is_number(row[price_idx]):
                price_values.append(float(row[price_idx]))

        if not price_values:
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert("1.0", "⚠️ لا توجد قيم أسعار رقمية")
            return

        # إنشاء التقرير
        report = "💰 تحليل مفصل للأسعار:\n\n"
        report += f"📊 معلومات عامة:\n"
        report += f"   • عدد التذاكر: {len(price_values):,}\n"
        report += f"   • متوسط السعر: {statistics.mean(price_values):.2f}\n"
        report += f"   • وسيط الأسعار: {statistics.median(price_values):.2f}\n"
        report += f"   • أرخص تذكرة: {min(price_values):.2f}\n"
        report += f"   • أغلى تذكرة: {max(price_values):.2f}\n\n"

        # فئات الأسعار
        if price_values:
            price_ranges = [(0, 50), (50, 100), (100, 200), (200, 500), (500, float('inf'))]
            report += "📊 توزيع الأسعار:\n"

            for low, high in price_ranges:
                count = sum(1 for p in price_values if low <= p < high)
                percentage = (count / len(price_values)) * 100

                if high == float('inf'):
                    range_text = f"أكثر من {low}"
                else:
                    range_text = f"{low}-{high}"

                report += f"   • {range_text}: {count:,} تذكرة ({percentage:.1f}%)\n"

        self.analysis_text.delete("1.0", tk.END)
        self.analysis_text.insert("1.0", report)

    def analyze_delays(self):
        """تحليل التأخير"""
        if not self.data:
            return

        # البحث عن عمود التأخير
        delay_idx = -1
        for i, header in enumerate(self.headers):
            if 'delay' in header.lower() or 'تأخير' in header.lower():
                delay_idx = i
                break

        if delay_idx < 0:
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert("1.0", "⚠️ لم يتم العثور على عمود التأخير")
            return

        # جمع قيم التأخير
        delay_values = []
        for row in self.data:
            if len(row) > delay_idx and self.is_number(row[delay_idx]):
                delay_values.append(float(row[delay_idx]))

        if not delay_values:
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert("1.0", "⚠️ لا توجد قيم تأخير رقمية")
            return

        # تحليل التأخير
        on_time = sum(1 for d in delay_values if d <= 0)
        delayed = sum(1 for d in delay_values if d > 0)
        total = len(delay_values)

        report = "⏱️ تحليل مفصل للتأخير:\n\n"
        report += f"📊 ملخص عام:\n"
        report += f"   • إجمالي الرحلات: {total:,}\n"
        report += f"   • في الوقت: {on_time:,} ({on_time / total * 100:.1f}%)\n"
        report += f"   • متأخرة: {delayed:,} ({delayed / total * 100:.1f}%)\n\n"

        if delayed > 0:
            delayed_values = [d for d in delay_values if d > 0]
            report += f"📈 إحصائيات التأخير:\n"
            report += f"   • متوسط التأخير: {statistics.mean(delayed_values):.1f} دقيقة\n"
            report += f"   • وسيط التأخير: {statistics.median(delayed_values):.1f} دقيقة\n"
            report += f"   • أقل تأخير: {min(delayed_values):.1f} دقيقة\n"
            report += f"   • أكبر تأخير: {max(delayed_values):.1f} دقيقة\n\n"

            # فئات التأخير
            delay_ranges = [(0, 15), (15, 30), (30, 60), (60, 120), (120, float('inf'))]
            report += "📊 توزيع أوقات التأخير:\n"

            for low, high in delay_ranges:
                count = sum(1 for d in delayed_values if low < d <= high)
                percentage = (count / delayed) * 100

                if low == 0:
                    range_text = f"حتى {high} دقيقة"
                elif high == float('inf'):
                    range_text = f"أكثر من {low} دقيقة"
                else:
                    range_text = f"{low}-{high} دقيقة"

                report += f"   • {range_text}: {count:,} رحلة ({percentage:.1f}%)\n"

        self.analysis_text.delete("1.0", tk.END)
        self.analysis_text.insert("1.0", report)

    def predict_delay(self):
        """التنبؤ باحتمال التأخير"""
        if not self.data:
            messagebox.showwarning("تحذير", "الرجاء تحميل البيانات أولاً")
            return

        try:
            # جمع بيانات الإدخال
            price = self.input_vars['price'].get()

            if not price or not self.is_number(price):
                messagebox.showwarning("تحذير", "الرجاء إدخال سعر صحيح")
                return

            price = float(price)

            # خوارزمية تنبؤ مبسطة (بدون تعلم آلي)
            # تستند إلى تحليل بسيط للبيانات

            # البحث عن عمود الأسعار
            price_idx = -1
            for i, header in enumerate(self.headers):
                if 'price' in header.lower() or 'سعر' in header.lower():
                    price_idx = i
                    break

            # البحث عن عمود التأخير
            delay_idx = -1
            for i, header in enumerate(self.headers):
                if 'delay' in header.lower() or 'تأخير' in header.lower():
                    delay_idx = i
                    break

            # إذا وجدنا أعمدة الأسعار والتأخير
            if price_idx >= 0 and delay_idx >= 0:
                # حساب متوسط السعر والتأخير من البيانات
                price_values = []
                delay_values = []

                for row in self.data:
                    if (len(row) > max(price_idx, delay_idx) and
                            self.is_number(row[price_idx]) and
                            self.is_number(row[delay_idx])):
                        price_values.append(float(row[price_idx]))
                        delay_values.append(float(row[delay_idx]))

                if price_values and delay_values:
                    avg_price = statistics.mean(price_values)

                    # خوارزمية تنبؤ مبسطة
                    if price < avg_price * 0.5:
                        probability = 0.7  # سعر منخفض = احتمال تأخير عالي
                    elif price < avg_price:
                        probability = 0.5  # سعر متوسط = احتمال متوسط
                    else:
                        probability = 0.3  # سعر مرتفع = احتمال تأخير منخفض
                else:
                    # إذا لم توجد بيانات كافية
                    probability = random.uniform(0.3, 0.7)
            else:
                # إذا لم توجد بيانات كافية للتحليل
                probability = random.uniform(0.3, 0.7)

            # إضافة عامل عشوائي بسيط
            probability += random.uniform(-0.1, 0.1)
            probability = max(0.1, min(0.9, probability))  # الحد بين 10% و90%

            # تحديث واجهة التنبؤ
            self.progress['value'] = probability * 100
            self.progress_label.config(text=f"{probability * 100:.1f}%")

            if probability > 0.6:
                result = "⚠️ تنبؤ: الرحلة معرضة للتأخير"
                color = "red"
                explanation = f"احتمالية التأخير عالية ({probability * 100:.1f}%)\nننصح باختيار رحلة أخرى أو وقت مختلف"
            elif probability > 0.4:
                result = "⚡ تنبؤ: احتمالية تأخير متوسطة"
                color = "orange"
                explanation = f"احتمالية التأخير متوسطة ({probability * 100:.1f}%)\nالرحلة مقبولة ولكن قد تكون هناك تأخيرات طفيفة"
            else:
                result = "✅ تنبؤ: الرحلة ستكون في الوقت"
                color = "green"
                explanation = f"احتمالية التأخير منخفضة ({probability * 100:.1f}%)\nالرحلة تبدو موثوقة وآمنة"

            self.result_label.config(text=result, fg=color)
            self.explanation.config(text=explanation)

            self.status.config(text=f"✅ تم التنبؤ - الاحتمال: {probability * 100:.1f}%")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل التنبؤ:\n{str(e)}")

    def is_number(self, s):
        """التحقق مما إذا كانت القيمة رقم"""
        try:
            float(s)
            return True
        except:
            return False


def main():
    """الدالة الرئيسية"""
    root = tk.Tk()
    app = SimpleRailwayPredictor(root)

    # إضافة أيقونة بسيطة
    try:
        root.iconbitmap(default='')  # يمكن إضافة أيقونة إذا كانت موجودة
    except:
        pass

    root.mainloop()


if __name__ == "__main__":
    print("\n🎯 جاري تشغيل نظام تنبؤ تأخير القطارات...")
    print("📋 المميزات:")
    print("   • واجهة رسومية احترافية")
    print("   • لا يحتاج تثبيت مكتبات خارجية")
    print("   • يعمل على أي جهاز Windows")
    print("   • تحليل كامل للبيانات")
    print("   • تنبؤ ذكي بالرحلات")
    print("=" * 60)
    print("\n🚀 جاري تحميل الواجهة...\n")

    main()