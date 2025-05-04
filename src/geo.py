import pandas as pd
import requests
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

archivo_cv = '../data/Listado.csv'
df = pd.read_csv(archivo_cv, delimiter=';')
df = df[["Provincia", "Localidad"]]
print(df.head())

conteo = df.value_counts().reset_index(name='Cantidad')
print(conteo)

save_path = '../data/conteo.csv'
conteo.to_csv(save_path, index=False)

# Ahora leemos el archivo agrupado
archivo_cv = '../data/conteo.csv'
df = pd.read_csv(archivo_cv, delimiter=',')
df = df[["Provincia", "Localidad", "Cantidad"]]

# Agregamos las columnas nuevas inicializadas como vacías
df["Latitud"] = ""
df["Longitud"] = ""

# Mostramos las primeras filas para verificar
print(df.head())

archivo_salida = '../data/conteo_con_coordenadas.csv'
df.to_csv(archivo_salida, index=False)
print(f"\nEl DataFrame con las nuevas columnas ha sido guardado en '{archivo_salida}'")

# Función para obtener latitud y longitud a partir de la dirección completa
def obtener_coordenadas(direccion):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={direccion}&format=json&limit=1"
        headers = {'User-Agent': 'mi_aplicacion/1.0 (miemail@ejemplo.com)'}  # Cambia por tu información
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]["lat"], data[0]["lon"]
            else:
                logging.warning(f"No se encontró la dirección: {direccion}")
                return None, None
        else:
            logging.error(f"Error en la solicitud: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Ocurrió un error en la solicitud: {e}")
        return None, None

# Creamos la dirección completa
df['direccion_completa'] = df[["Provincia", "Localidad"]].agg(', '.join, axis=1)

# Recorremos cada fila y actualizamos las coordenadas en el DataFrame
for idx, row in df.iterrows():
    direccion = row['direccion_completa']
    latitud, longitud = obtener_coordenadas(direccion)
    if latitud is not None and longitud is not None:
        df.at[idx, 'Latitud'] = latitud
        df.at[idx, 'Longitud'] = longitud
        print(f"Coordenadas de {direccion}: Latitud: {latitud}, Longitud: {longitud}")
    else:
        print(f"No se pudieron obtener las coordenadas para: {direccion}")

# Guardamos el DataFrame actualizado con coordenadas
df.to_csv('../data/conteo_con_coordenadas.csv', index=False)
print("\nEl archivo con las coordenadas ha sido guardado como 'conteo_con_coordenadas.csv'")
