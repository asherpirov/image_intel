# מייבאים את הפונקציה שכתבתם מתוך תיקיית src
from src.extractor import extract_all

# נתיב לתיקיית התמונות של הפרויקט (ראיתי בתמונה שלך שיש תיקיית images)
folder_path = r"C:\Users\User\PycharmProjects\image-Intel\image_intel-main\image_intel-main\images\sample_data"
print("מתחיל סריקת תמונות...")
results = extract_all(folder_path)

print(f"מצאתי {len(results)} תמונות! הנה הנתונים:")
print("-" * 30)

# מדפיס את התוצאות בצורה יפה
for item in results:
    print(f"קובץ: {item['filename']}")
    print(f"זמן: {item['datetime']}")
    print(f"מצלמה: {item['camera_make']} {item['camera_model']}")
    print(f"מיקום GPS: {item['latitude']}, {item['longitude']}")
    print("-" * 30)