from PIL import Image
from PIL.ExifTags import TAGS
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A
גרסה מפושטת וקלה לקריאה
"""


def dms_to_decimal(dms, ref):
    """
    פונקציית עזר שמחשבת את ה-GPS ממספרים מוזרים (מעלות, דקות, שניות) למספר עשרוני
    """
    try:
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1]
        seconds = dms[2][0] / dms[2][1]

        result = degrees + (minutes / 60) + (seconds / 3600)

        # אם זה דרום או מערב, המספר צריך להיות שלילי
        if ref == 'S' or ref == 'W':
            result = result * -1

        return round(result, 6)
    except:
        return None


def has_gps(data: dict):
    # בודק פשוט אם המילה "GPSInfo" קיימת במילון הנתונים
    if "GPSInfo" in data:
        return True
    return False


def latitude(data: dict):
    if has_gps(data):
        gps_info = data["GPSInfo"]
        # 2 = קו רוחב, 1 = כיוון (צפון/דרום)
        if 2 in gps_info and 1 in gps_info:
            return dms_to_decimal(gps_info[2], gps_info[1])
    return None


def longitude(data: dict):
    if has_gps(data):
        gps_info = data["GPSInfo"]
        # 4 = קו אורך, 3 = כיוון (מזרח/מערב)
        if 4 in gps_info and 3 in gps_info:
            return dms_to_decimal(gps_info[4], gps_info[3])
    return None


def datatime(data: dict):
    if "DateTimeOriginal" in data:
        return data["DateTimeOriginal"]
    return None


def camera_make(data: dict):
    if "Make" in data:
        # str() הופך לטקסט, replace מנקה תווים נסתרים אם יש
        return str(data["Make"]).replace('\x00', '')
    return None


def camera_model(data: dict):
    if "Model" in data:
        return str(data["Model"]).replace('\x00', '')
    return None


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.
    """
    # 1. מכינים מילון התחלתי וריק ליתר ביטחון
    filename = os.path.basename(image_path)
    result = {
        "filename": filename,
        "datetime": None,
        "latitude": None,
        "longitude": None,
        "camera_make": None,
        "camera_model": None,
        "has_gps": False
    }

    try:
        # 2. מנסים לפתוח את התמונה
        img = Image.open(image_path)
        exif_raw = img._getexif()

        if exif_raw is not None:
            # 3. מתרגמים את המספרים של EXIF למילים קריאות באנגלית
            clean_data = {}
            for tag_id, value in exif_raw.items():
                tag_name = TAGS.get(tag_id, tag_id)
                clean_data[tag_name] = value

            # 4. מעדכנים את המילון בעזרת הפונקציות הפשוטות שכתבנו למעלה
            result["datetime"] = datatime(clean_data)
            result["latitude"] = latitude(clean_data)
            result["longitude"] = longitude(clean_data)
            result["camera_make"] = camera_make(clean_data)
            result["camera_model"] = camera_model(clean_data)
            result["has_gps"] = has_gps(clean_data)

    except:
        # אם התמונה שבורה או שאין לה נתונים, פשוט נחזיר את המילון הריק שהכנו
        pass

    return result


def extract_all(folder_path):
    """
    עובר על כל התמונות בתיקייה ואוסף את הנתונים שלהן לרשימה.
    """
    all_results = []

    # מוודא שהתיקייה באמת קיימת
    if not os.path.exists(folder_path):
        return all_results

    # עובר בלולאה על כל הקבצים בתיקייה
    for filename in os.listdir(folder_path):
        # בודק שזה קובץ תמונה רגיל
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            full_path = os.path.join(folder_path, filename)
            data = extract_metadata(full_path)
            all_results.append(data)

    return all_results