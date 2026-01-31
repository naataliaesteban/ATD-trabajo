# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:00:42 2026

@author: 46mjn
"""

import requests
import time


api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0Nm1qbmF0YWxpYUBnbWFpbC5jb20iLCJqdGkiOiJmYTBjMDk1NS05Y2UxLTRjMjktOGMwOC1jM2M0N2Y0NmE4NzciLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2ODY1MTM1NCwidXNlcklkIjoiZmEwYzA5NTUtOWNlMS00YzI5LThjMDgtYzNjNDdmNDZhODc3Iiwicm9sZSI6IiJ9.SpN2yy9LWwUUwmP-NI6Qxpg4syJRO7jWkDZ4aj1d9_k'


def obtener_clima_ciudad(fecha_ini, fecha_fin, id_estacion):
    url_pedido = (
        "https://opendata.aemet.es/opendata/api/"
        f"valores/climatologicos/diarios/datos/"
        f"fechaini/{fecha_ini}T00:00:00UTC/"
        f"fechafin/{fecha_fin}T23:59:59UTC/"
        f"estacion/{id_estacion}"
    )

    headers = {'api_key': api_key}

    try:
        # PASO 1: pedir permiso a la API
        res = requests.get(url_pedido, headers=headers)
        res_json = res.json()

        if res_json.get('estado') == 200:
            url_datos = res_json.get('datos')

            if url_datos is None:
                print(f"El servidor aún está procesando los datos de {id_estacion}.")
                return []

            # PASO 2: descargar datos reales (pausa de seguridad)
            time.sleep(3)
            datos_finales = requests.get(url_datos).json()

            # PASO 3: limpiar datos
            limpios = []
            for d in datos_finales:
                limpios.append({
                    'fecha': d.get('fecha'),
                    'tmed': d.get('tmed'),  # temperatura media
                    'prec': d.get('prec')   # precipitación
                })
            return limpios

        else:
            print("Error API:", res_json.get('descripcion'))
            return []

    except Exception as e:
        print("Error de conexión:", e)
        return []


ID_BARCELONA = "0076"  # Barcelona (Fabra)

print(" Obteniendo Invierno (Barcelona)...")
invierno_bcn = obtener_clima_ciudad("2024-01-01", "2024-01-31", ID_BARCELONA)

# Pausa obligatoria de 10 segundos para evitar bloqueo de la API
print(" Esperando 10 segundos para no saturar la API...")
time.sleep(10)

print(" Obteniendo Verano (Barcelona)...")
verano_bcn = obtener_clima_ciudad("2024-07-01", "2024-07-31", ID_BARCELONA)

# =============================
# MOSTRAR RESULTADOS
# =============================
print("\n  INVIERNO (ENERO) - BARCELONA")
for d in invierno_bcn:
    print(d)

print("\n  VERANO (JULIO) - BARCELONA")
for d in verano_bcn:
    print(d)

# =============================
# FUNCIÓN EXTRA: MEDIA TEMPERATURA
# =============================
def media_temperatura(datos):
    temperaturas = []
    for d in datos:
        tmed_valor = d.get('tmed')
        if tmed_valor is not None:
            try:
                num = float(tmed_valor.replace(',', '.'))
                temperaturas.append(num)
            except ValueError:
                continue
    
    if len(temperaturas) == 0:
        return 0
    return sum(temperaturas) / len(temperaturas)

if invierno_bcn and verano_bcn:
    print("\n TEMPERATURAS MEDIAS EN BARCELONA")
    print(f"Media Invierno: {media_temperatura(invierno_bcn):.2f} °C")
    print(f"Media Verano: {media_temperatura(verano_bcn):.2f} °C")