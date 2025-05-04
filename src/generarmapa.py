import folium
import pandas as pd

# Leer el archivo
archivo = "../data/conteo_con_coordenadas.csv"
df = pd.read_csv(archivo)

# Convertir columnas a número por si acaso
df["Latitud"] = pd.to_numeric(df["Latitud"], errors='coerce')
df["Longitud"] = pd.to_numeric(df["Longitud"], errors='coerce')
df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors='coerce')

# Filtrar filas con coordenadas válidas
df = df.dropna(subset=["Latitud", "Longitud"])

# Crear el mapa (puedes centrarlo donde prefieras)
mapa = folium.Map(location=[df["Latitud"].mean(), df["Longitud"].mean()], zoom_start=6)

# Definir función para elegir color según cantidad
def elegir_color(cantidad):
    if cantidad < 10:
        return 'green'
    elif cantidad < 50:
        return 'orange'
    else:
        return 'red'

# Agregar marcadores al mapa
for _, row in df.iterrows():
    color = elegir_color(row["Cantidad"])
    popup_text = f"{row['Provincia']}, {row['Localidad']}<br>Cantidad: {row['Cantidad']}"
    folium.CircleMarker(
        location=[row["Latitud"], row["Longitud"]],
        radius=7,  # tamaño del círculo
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=popup_text
    ).add_to(mapa)

# (Opcional) Capa de calor
# from folium.plugins import HeatMap
# heat_data = [[row["Latitud"], row["Longitud"], row["Cantidad"]] for _, row in df.iterrows()]
# HeatMap(heat_data).add_to(mapa)

# Guardar el mapa
mapa.save("../output/mapa_con_marcadores_coloreados.html")

print("Mapa guardado en 'mapa_con_marcadores_coloreados.html'")
