# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:17:57 2026

@author: naataliaesteban
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
                print("El servidor aún está procesando los datos.")
                return []

            # PASO 2: descargar datos reales
            time.sleep(2)
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
            print("Error:", res_json.get('descripcion'))
            return []

    except Exception as e:
        print("Error:", e)
        return []


ID_SEVILLA = "5783"  # Sevilla Aeropuerto


invierno_sevilla = obtener_clima_ciudad(
    fecha_ini="2024-01-01",
    fecha_fin="2024-01-31",
    id_estacion=ID_SEVILLA
)


verano_sevilla = obtener_clima_ciudad(
    fecha_ini="2024-07-01",
    fecha_fin="2024-07-31",
    id_estacion=ID_SEVILLA
)


print(" INVIERNO (ENERO)")
for d in invierno_sevilla:
    print(d)

print("\n VERANO (JULIO)")
for d in verano_sevilla:
    print(d)


def media_temperatura(datos):
    temperaturas = []
    for d in datos:
        if d['tmed'] is not None:
            temperaturas.append(float(d['tmed'].replace(',', '.')))
    return sum(temperaturas) / len(temperaturas)

print("\n TEMPERATURAS MEDIAS")
print("Invierno:", media_temperatura(invierno_sevilla))
print("Verano:", media_temperatura(verano_sevilla))

