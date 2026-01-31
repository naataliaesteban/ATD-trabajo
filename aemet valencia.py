# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:42:11 2026

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
        res = requests.get(url_pedido, headers=headers)
        res_json = res.json()

        if res_json.get('estado') == 200:
            url_datos = res_json.get('datos')

            if url_datos is None:
                print("El servidor aún está procesando los datos.")
                return []

            
            time.sleep(2)
            datos_finales = requests.get(url_datos).json()

            
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


ID_VALENCIA = "8416"  # Valencia (Viveros)


invierno_valencia = obtener_clima_ciudad(
    fecha_ini="2024-01-01",
    fecha_fin="2024-01-31",
    id_estacion=ID_VALENCIA
)


verano_valencia = obtener_clima_ciudad(
    fecha_ini="2024-07-01",
    fecha_fin="2024-07-31",
    id_estacion=ID_VALENCIA
)


print(" INVIERNO (ENERO) - VALENCIA")
for d in invierno_valencia:
    print(d)

print("\n VERANO (JULIO) - VALENCIA")
for d in verano_valencia:
    print(d)

def media_temperatura(datos):
    temperaturas = []
    for d in datos:
        if d['tmed'] is not None:
            # Reemplaza la coma por punto para poder convertir a float
            temperaturas.append(float(d['tmed'].replace(',', '.')))
    
    if not temperaturas:
        return 0
    return sum(temperaturas) / len(temperaturas)

print("\n TEMPERATURAS MEDIAS EN VALENCIA")
print(f"Media Invierno: {media_temperatura(invierno_valencia):.2f} °C")
print(f"Media Verano: {media_temperatura(verano_valencia):.2f} °C")



