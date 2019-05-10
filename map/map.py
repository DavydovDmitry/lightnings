import folium


def build_map():
    map = folium.Map(location=[60.25, 24.8], tiles='Stamen Toner',
                   zoom_start=15, control_scale=True)
    map.save('map.html')

if __name__ == "__main__":
    build_map()