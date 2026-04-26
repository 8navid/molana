# ============================================================
# نصب کتابخونه‌های مورد نیاز :
# pip install pandas wordcloud matplotlib
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import time


# برای پشتیبانی صحیح از حروف فارسی (راست‌به‌چپ)
import arabic_reshaper
from bidi.algorithm import get_display

# ============================================================
# 1. بارگذاری دیتاست از فایل CSV (اشعار مولانا)
# ============================================================
start_time = time.time()

print("📂 در حال بارگذاری دیتاست اشعار مولانا...")
df = pd.read_csv("Clustering-Mowlana-poemWise.csv")  # فایل CSV که دانلود کردی
poem_texts = df['Poem'].dropna().tolist()  # فقط ستون Poem (متن شعر) رو برمی‌داریم

print(f"✅ تعداد اشعار: {len(poem_texts)}")

# ============================================================
# 2. تعریف کلمات ایست (stop words) فارسی
# ============================================================
def load_stopwords(file_path):
    """لود کردن استاپ‌وردها از فایل متنی"""
    with open(file_path, 'r', encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f if line.strip())
    return stopwords

# فایل persian.txt رو کنار کد پایتون بذار
persian_stop_words = load_stopwords("persian.txt")
print(f"🛑 تعداد ایست‌واژه‌ها: {len(persian_stop_words)}")

# ============================================================
# 3. تابع تمیز کردن متن
# ============================================================
def clean_text(text):
    """
    این تابع متن رو تمیز می‌کنه:
    - علائم نگارشی رو حذف می‌کنه
    - فقط حروف و فاصله رو نگه می‌داره
    - متن رو به کلمات تقسیم می‌کنه
    - کلمات کوتاه (کمتر از ۲ حرف) و ایست‌واژه‌ها رو حذف می‌کنه
    """
    # حذف اعداد و علائم نگارشی
    text = re.sub(r'[^\w\s]', ' ', str(text))
    text = re.sub(r'\d+', ' ', text)
    
    # تبدیل به لیست کلمات
    words = text.split()
    
    # فیلتر کردن: حذف کلمات کوتاه و ایست‌واژه‌ها
    cleaned = []
    for word in words:
        if len(word) >= 2 and word not in persian_stop_words:
            cleaned.append(word)
    
    return cleaned

# ============================================================
# 4. شمارش کلمات در کل اشعار
# ============================================================
print("🔢 در حال شمارش کلمات...")
all_words = []

for text in poem_texts:
    all_words.extend(clean_text(text))

# شمارش فراوانی
word_counts = Counter(all_words)

# ============================================================
# 5. نمایش ۲۰ کلمه پرتکرار
# ============================================================
print("\n📊 ۲۰ کلمه پرتکرار در اشعار مولانا:")
print("-" * 40)
top_words = word_counts.most_common(20)
for i, (word, count) in enumerate(top_words, 1):
    # اصلاح حروف برای نمایش درست فارسی در ترمینال
    reshaped = arabic_reshaper.reshape(word)
    bidi_word = get_display(reshaped)
    print(f"{i:2d}. {bidi_word}: {count} بار")

# ============================================================
# 6. رسم WordCloud
# ============================================================
print("\n🎨 در حال رسم WordCloud...")

# تبدیل کلمات به شکل مناسب برای نمایش فارسی در WordCloud
reshaped_frequencies = {}
for word, freq in word_counts.items():
    reshaped_word = arabic_reshaper.reshape(word)
    bidi_word = get_display(reshaped_word)
    reshaped_frequencies[bidi_word] = freq

# تنظیمات WordCloud
wordcloud = WordCloud(
    width=1200,           # عرض تصویر
    height=800,           # ارتفاع تصویر
    background_color='white',  # پس‌زمینه سفید
    font_path='Vazirmatn-Light.ttf',     # فونت فارسی
    max_words=200,        # حداکثر تعداد کلمات
    max_font_size=150,    # حداکثر سایز فونت
    collocations=False,   # ترکیب‌های دوکلمه‌ای رو نشون نده
).generate_from_frequencies(reshaped_frequencies)

# نمایش
plt.figure(figsize=(14, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # حذف محورها
plt.title('WordCloud اشعار مولانا - پرتکرارترین کلمات', fontsize=18)
plt.tight_layout(pad=0)

# ذخیره تصویر
plt.savefig('wordcloud_mowlana.png', dpi=150, bbox_inches='tight')
print("✅ تصویر WordCloud ذخیره شد: wordcloud_mowlana.png")

plt.show()

end_time = time.time()
execution_time = end_time - start_time

# ============================================================
# 7.1. تحلیل اضافه: چند شعر شامل کلمه "عشق" هستن؟
# ============================================================
keyword = "عشق"
count = 0
for text in poem_texts:
    if keyword in str(text):
        count += 1

print(f"\n🔍 شعرهای شامل کلمه '{keyword}': {count} از {len(poem_texts)} شعر")


# ============================================================
# 7.2. تحلیل اضافه: چند شعر شامل کلمه "فراق" هستن؟
# ============================================================
keyword2 = "فراق"
count2 = 0
for text in poem_texts:
    if keyword2 in str(text):
        count2 += 1

print(f"\n🔍 شعرهای شامل کلمه '{keyword2}': {count2} از {len(poem_texts)} شعر")

# ============================================================
# 8. خلاصه نهایی برای ارائه
# ============================================================
print("\n" + "="*50)
print("📋 خلاصه برای ارائه:")
print("="*50)
print(f"• تعداد کل اشعار: {len(poem_texts)}")
print(f"• تعداد کل کلمات (بدون ایست‌واژه): {len(all_words):,}")
print(f"• کلمات یکتا: {len(word_counts):,}")
print(f"• کلمه پرتکرار اول: '{top_words[0][0]}' با {top_words[0][1]} بار")
print("• خروجی: wordcloud_mowlana.png")

# ============================================================
# 9. تولید فایل گزارش کامل (TXT)
# ============================================================
print("\n📝 در حال ساخت فایل گزارش...")

with open('report_mowlana.txt', 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("📊 گزارش تحلیل اشعار مولانا - WordCloud\n")
    f.write(f"\n⏱️ مدت زمان اجرا: {execution_time:.2f} ثانیه\n")
    f.write("="*60 + "\n\n")
    
    f.write(f"نام دیتاست: Persian-poetry (Clustering-Mowlana-poemWise.csv)\n")
    f.write(f"شاعر: مولانا\n")
    f.write(f"تعداد کل اشعار: {len(poem_texts)}\n")
    f.write(f"تعداد کل کلمات (بدون ایست‌واژه): {len(all_words):,}\n")
    f.write(f"تعداد کلمات یکتا: {len(word_counts):,}\n\n")
    
    f.write("-"*40 + "\n")
    f.write("۲۰ کلمه پرتکرار در اشعار مولانا:\n")
    f.write("-"*40 + "\n")
    for i, (word, count) in enumerate(top_words, 1):
        f.write(f"{i:2d}. {word}: {count} بار\n")
    
    f.write("\n" + "-"*40 + "\n")
    f.write(f"تحلیل موردی - کلمه '{keyword}':\n")
    f.write("-"*40 + "\n")
    f.write(f"در {count} شعر از {len(poem_texts)} شعر آمده است.\n")
    f.write(f"درصد: {count/len(poem_texts)*100:.1f}%\n\n")

    f.write("\n" + "-"*40 + "\n")
    f.write(f"تحلیل موردی - کلمه '{keyword2}':\n")
    f.write("-"*40 + "\n")
    f.write(f"در {count2} شعر از {len(poem_texts)} شعر آمده است.\n")
    f.write(f"درصد: {count2/len(poem_texts)*100:.1f}%\n\n")
    

print("✅ فایل report_mowlana.txt ذخیره شد.")
