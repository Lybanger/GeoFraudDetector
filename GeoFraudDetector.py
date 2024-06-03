import folium
import folium.plugins as fp
import pandas as pd

df = pd.read_csv("geos.csv")
df2 = pd.read_csv("fraude.csv")
min_lat = min(df[['Latitud_Sup_Izq', 'Latitud_Inf_Der']].min()) + 1.5
min_lon = min(df[['Longitud_Sup_Izq', 'Longitud_Inf_Der']].min()) + 1.5
max_lat = max(df[['Latitud_Sup_Izq', 'Latitud_Inf_Der']].max()) + 1.5
max_lon = max(df[['Longitud_Sup_Izq', 'Longitud_Inf_Der']].max()) + 1.5

m = fp.DualMap(
    tiles="cartodb positron",
    location=(13.931975, -89.192584),
    max_bounds=False,
    zoom_start=4,
    min_lat=min_lat,
    max_lat=max_lat,
    min_lon=min_lon,
    max_lon=max_lon,
)


def geo_cercas(df, mapa, mapa1):
    for index, row in df.iterrows():
        if row['Current Status'] == "Production":
            coordenadas = [
                [row['Latitud_Sup_Izq'], row['Longitud_Sup_Izq']],
                [row['Latitud_Sup_Izq'], row['Longitud_Inf_Der']],
                [row['Latitud_Inf_Der'], row['Longitud_Inf_Der']],
                [row['Latitud_Inf_Der'], row['Longitud_Sup_Izq']],
                [row['Latitud_Sup_Izq'], row['Longitud_Sup_Izq']]
            ]
            Color = "blue"
            polyline = folium.PolyLine(locations=coordenadas, color=Color)
            popup_text = f"Datos de {row['Rule Name']} descripción: {row['Description']}"
            popup = folium.Popup(popup_text)
            polyline.add_child(popup)
            polyline.add_to(mapa)
        elif row['Current Status'] == "Test":
            coordenadas = [
                [row['Latitud_Sup_Izq'], row['Longitud_Sup_Izq']],
                [row['Latitud_Sup_Izq'], row['Longitud_Inf_Der']],
                [row['Latitud_Inf_Der'], row['Longitud_Inf_Der']],
                [row['Latitud_Inf_Der'], row['Longitud_Sup_Izq']],
                [row['Latitud_Sup_Izq'], row['Longitud_Sup_Izq']]
            ]
            Color = "orange"
            polyline = folium.PolyLine(locations=coordenadas, color=Color)
            popup_text = f"Datos de {row['Rule Name']} descripción: {row['Description']}"
            popup = folium.Popup(popup_text)
            polyline.add_child(popup)
            polyline.add_to(mapa1)


def activaciones(df, mapa, mapa1):
    marker_cluster = fp.MarkerCluster(name="Produccion")
    mapa.add_child(marker_cluster)

    marker_cluster1 = fp.MarkerCluster(name="Test")
    mapa1.add_child(marker_cluster1)
    for geo_status in df['status'].unique():
        geos_values = df[df['status'] == geo_status]['Geo'].unique()

        if geo_status == 'Produccion':
            for geo_value in geos_values:
                group = fp.FeatureGroupSubGroup(marker_cluster, geo_value, show=True)
                mapa.add_child(group)

                # Filtrar los datos para ese valor de "Geo"
                filtered_data = df[(df['Geo'] == geo_value) & (df['status'] == 'Produccion')]

                # Agregar marcadores al grupo correspondiente
                for index, row in filtered_data.iterrows():
                    # Condicionantes de colores por marcación
                    coordenadas = [row['Latitude'], row['Longitude']]
                    if row['Final'] == "CONFIRMED_FRAUD":
                        icon = folium.Icon(color='red', icon='star')
                    elif row['Final'] == "SUSPECTED_FRAUD":
                        icon = folium.Icon(color='lightred', icon='star')
                    elif row['Final'] == "CONFIRMED_GENUINE":
                        icon = folium.Icon(color='green', icon='star')
                    elif row['Final'] == "ASSUMED_GENUINE":
                        icon = folium.Icon(color='lightgreen', icon='star')
                    else:
                        icon = folium.Icon(color='lightgray', icon='star')
                    marker = folium.Marker(location=coordenadas, icon=icon)
                    popup_text = f"Canal {row['Canal']} - Resolución: {row['Final']}"
                    popup = folium.Popup(popup_text)
                    marker.add_child(popup)
                    gg = marker.add_child(popup)
                    gg.add_to(group)

        elif geo_status == 'Test':
            for geo_value in geos_values:
                group = fp.FeatureGroupSubGroup(marker_cluster1, geo_value, show=True)
                mapa1.add_child(group)

                # Filtrar los datos para ese valor de "Geo"
                filtered_data = df[(df['Geo'] == geo_value) & (df['status'] == 'Test')]

                # Agregar marcadores al grupo correspondiente
                for index, row in filtered_data.iterrows():
                    # Condicionantes de colores por marcación
                    coordenadas = [row['Latitude'], row['Longitude']]
                    if row['Final'] == "CONFIRMED_FRAUD":
                        icon = folium.Icon(color='red', icon='star')
                    elif row['Final'] == "SUSPECTED_FRAUD":
                        icon = folium.Icon(color='lightred', icon='star')
                    elif row['Final'] == "CONFIRMED_GENUINE":
                        icon = folium.Icon(color='green', icon='star')
                    elif row['Final'] == "ASSUMED_GENUINE":
                        icon = folium.Icon(color='lightgreen', icon='star')
                    else:
                        icon = folium.Icon(color='lightgray', icon='star')
                    marker = folium.Marker(location=coordenadas, icon=icon)
                    popup_text = f"Canal {row['Canal']} - Resolución: {row['Final']}"
                    popup = folium.Popup(popup_text)
                    marker.add_child(popup)
                    gg = marker.add_child(popup)
                    gg.add_to(group)


geo_cercas(df, m.m1, m.m2)
activaciones(df2, m.m1, m.m2)
folium.LayerControl().add_to(m)
m










