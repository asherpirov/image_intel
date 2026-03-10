import folium


def create_map(images_data):
    gps_images = [img for img in images_data if img["has_gps"]]

    if not gps_images:
        return "<h2>No GPS data found</h2>"
    gps_images.sort(key=lambda x: x['datetime'])  #ממיין את המיקומים לפי הזמן שצולמו למתיחת קווים


    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    for img in gps_images:
        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=f"{img['filename']}<br>{img['datetime']}<br>{img['camera_model']}",
        ).add_to(m)
    #מתיחת קווים
    path_coords = [[img["latitude"], img["longitude"]] for img in gps_images]
    folium.PolyLine(path_coords, color="blue", weight=2, opacity=0.8).add_to(m)

    m.save("my_map.html")
    return m._repr_html_()









