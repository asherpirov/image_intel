from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.
"""


def dms_to_decimal(dms_tuple, ref):
    """
    פונקציית עזר (מהמדריך שלכם) שממירה את הקואורדינטות של ה-GPS
    מפורמט של מעלות/דקות/שניות למספר עשרוני נקי למפה.
    """
    try:
        def get_val(v):
            return v[0] / v[1] if isinstance(v, tuple) else float(v)

        degrees = get_val(dms_tuple[0])
        minutes = get_val(dms_tuple[1])
        seconds = get_val(dms_tuple[2])

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        # אם המיקום הוא דרום (S) או מערב (W), המספר צריך להיות שלילי
        if ref in ['S', 'W', b'S', b'W']:
            decimal = -decimal
        return round(decimal, 6)
    except Exception:
        return None


def has_gps(data: dict):
    # בודק אם יש למצלמה מידע על מיקום (GPSInfo)
    # ומוודא שיש שם גם קו רוחב (2) וגם קו אורך (4)
    if "GPSInfo" not in data:
        return False
    gps_info = data["GPSInfo"]
    return 2 in gps_info and 4 in gps_info


def latitude(data: dict):
    if not has_gps(data):
        return None
    gps_info = data["GPSInfo"]
    # 2 = Latitude (קו רוחב), 1 = N/S (צפון/דרום)
    return dms_to_decimal(gps_info[2], gps_info.get(1, 'N'))


def longitude(data: dict):
    if not has_gps(data):
        return None
    gps_info = data["GPSInfo"]
    # 4 = Longitude (קו אורך), 3 = E/W (מזרח/מערב)
    return dms_to_decimal(gps_info[4], gps_info.get(3, 'E'))


def datatime(data: dict):
    # שולף את תאריך ושעת הצילום
    return data.get("DateTimeOriginal") or data.get("DateTime")


def camera_make(data: dict):
    make = data.get("Make")
    # מנקה את הטקסט למקרה שהמצלמה שומרת אותו בפורמט מוזר
    if make and isinstance(make, bytes):
        return make.decode(errors="ignore").strip('\x00')
    return str(make).strip('\x00') if make else None


def camera_model(data: dict):
    model = data.get("Model")
    if model and isinstance(model, bytes):
        return model.decode(errors="ignore").strip('\x00')
    return str(model).strip('\x00') if model else None


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.
    """
    path = Path(image_path)

    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה ומחזיר רשימה של מילונים.
    """
    results = []
    path = Path(folder_path)

    # מוודא שהתיקייה באמת קיימת
    if not path.exists() or not path.is_dir():
        return results

    # עובר על כל הקבצים בתיקייה ומפעיל את extract_metadata רק על תמונות
    for file_path in path.iterdir():
        if file_path.suffix.lower() in ['.jpg', '.jpeg']:
            results.append(extract_metadata(str(file_path)))

    return results