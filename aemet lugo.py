# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:10 2026

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
            time.sleep(3) # Espera crítica para que el servidor genere el JSON
            
            respuesta_datos = requests.get(url_datos)
            if respuesta_datos.status_code == 200:
                return respuesta_datos.json()
            return []
        else:
            print(f"Aviso para {fecha_ini}: {res_json.get('descripcion')}")
            return []
    except Exception as e:
        print("Error:", e)
        return []


ID_LUGO_CIUDAD = "1014A" 

print(" Consultando Lugo Ciudad (Enero)...")
invierno_lugo = obtener_clima_ciudad("2024-01-01", "2024-01-31", ID_LUGO_CIUDAD)

time.sleep(10) # Pausa más larga para evitar el bloqueo de caudal

print(" Consultando Lugo Ciudad (Julio)...")
verano_lugo = obtener_clima_ciudad("2024-07-01", "2024-07-31", ID_LUGO_CIUDAD)


def procesar_y_mostrar(datos, titulo):
    print(f"\n{titulo}")
    temperaturas = []
    if not datos:
        print("Sin datos disponibles.")
        return 0
    
    for d in datos:
        print(d)
        if d.get('tmed'):
            temperaturas.append(float(d['tmed'].replace(',', '.')))
    
    return sum(temperaturas) / len(temperaturas) if temperaturas else 0

media_inv = procesar_y_mostrar(invierno_lugo, " INVIERNO")
media_ver = procesar_y_mostrar(verano_lugo, "VERANO")

if media_inv and media_ver:

    print(f"\n MEDIAS LUGO: Invierno {media_inv:.2f}°C | Verano {media_ver:.2f}°C")
