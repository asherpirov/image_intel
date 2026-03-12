"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""
import folium


def get_clean_gps_data(raw_images_data):
    """
    לוקחת את הרשימה הגולמית מה-Extractor ומחזירה רק מה שראוי להצגה על מפה.
    """
    clean_list = []

    for img in raw_images_data:
        #  והאם יש לה GPS בדיקה שהתמונה בכלל קיימת ויש לה קואורדינטות מספריות
        if img.get("has_gps") and \
                isinstance(img.get("latitude"), (int, float)) and \
                isinstance(img.get("longitude"), (int, float)):
            clean_list.append(img)

        return clean_list


#מיון הנתונים לפי זמן
def sort_by_time(arr):
    return arr.sort(key=lambda x: x['datetime'])



def add_map_elements(map_object,gps_images):
    for img in gps_images:
        #במידה ויש מפתח שאין בו ערך
        filename = img.get("filename", "Unknown File")
        dt = img.get("datetime", "Date Unknown")
        model = img.get("camera_model", "Generic Device")
        popup_content = f"<b>File:</b> {filename}<br><b>Time:</b> {dt}<br><b>Device:</b> {model}"

        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup= popup_content,
            ).add_to(map_object)
    # מתיחת קווים
    path_coords = [[img["latitude"], img["longitude"]] for img in gps_images]
    folium.PolyLine(path_coords, color="blue", weight=2, opacity=0.8).add_to(map_object)
    ##הערה:נשאר רק לתת צבע לכול מכשיר שונה תוכל להתחיל מכאן


def create_map(images_data):
    gps_images = get_clean_gps_data(images_data)

    if not gps_images:
        return "<h2>No GPS data found</h2>"
    #חישוב מרכז מפה
    center_lat = sum([img["latitude"] for img in gps_images  ]) / len(gps_images)
    center_lon = sum([img["longitude"] for img in gps_images ]) / len(gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    add_map_elements(m,gps_images)

    return m._repr_html_()







    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    pass



if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
#קובץ לבדיקה
#html = create_map(fake_data)
#with open("test_map.html", "w", encoding="utf-8") as f:
 #   f.write(html)
 #   print("Map saved to test_map.html")
