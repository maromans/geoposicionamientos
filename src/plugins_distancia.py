import folium
import pandas as pd
from folium.plugins import MeasureControl

# Leer archivo
archivo = "conteo_con_coordenadas.csv"
df = pd.read_csv(archivo)

df["Latitud"] = pd.to_numeric(df["Latitud"], errors='coerce')
df["Longitud"] = pd.to_numeric(df["Longitud"], errors='coerce')
df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors='coerce')

df = df.dropna(subset=["Latitud", "Longitud"])

# Crear mapa centrado
mapa = folium.Map(location=[df["Latitud"].mean(), df["Longitud"].mean()], zoom_start=6)

# Agregar control de medición
mapa.add_child(MeasureControl(primary_length_unit='kilometers'))

# Definir color por cantidad
def elegir_color(cantidad):
    if cantidad < 10:
        return 'green'
    elif cantidad < 50:
        return 'orange'
    else:
        return 'red'

# Agregar marcadores
for _, row in df.iterrows():
    color = elegir_color(row["Cantidad"])
    popup_text = f"{row['Provincia']}, {row['Localidad']}<br>Cantidad: {row['Cantidad']}"
    tooltip_text = f"Cantidad: {row['Cantidad']}"
    
    folium.CircleMarker(
        location=[row["Latitud"], row["Longitud"]],
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=tooltip_text
    ).add_to(mapa)

# Guardar mapa
mapa.save("mapa_con_medicion.html")

print("Mapa guardado en 'mapa_con_medicion.html'")
