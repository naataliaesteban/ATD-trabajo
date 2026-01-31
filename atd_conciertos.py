# -*- coding: utf-8 -*-
"""
@author: qrnnx
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def main():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    cities = {
        "Valencia": "https://lineapp.live/locations/valencia/past-events",
        "Madrid": "https://lineapp.live/locations/madrid/past-events",
        "Barcelona": "https://lineapp.live/locations/barcelona/past-events",
        "Sevilla": "https://lineapp.live/locations/sevilla/past-events",
        "Lugo": "https://lineapp.live/locations/lugo/past-events"
    }

    all_concerts = []

    try:
        print("=== SCRAPING CONCIERTOS PASADOS ===")

        for city, base_url in cities.items():
            print(f"\ Ciudad: {city}")
            page = 1

            while True:
                url = f"{base_url}?page={page}"
                print(f" Página {page}")
                driver.get(url)

                try:
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                except:
                    print("No carga la página")
                    break

                time.sleep(3)

                eventos = driver.find_elements(By.CSS_SELECTOR, "a[href*='/events/']")

                if not eventos:
                    print("No hay más páginas")
                    break

                encontrados = 0

                for evento in eventos:
                    texto = evento.text.strip()
                    if texto and len(texto) > 10:
                        lineas = texto.split("\n")

                        all_concerts.append({
                            "Ciudad": city,
                            "Evento": lineas[0],
                            "Fecha": lineas[1] if len(lineas) > 1 else None,
                            "Sala": lineas[2] if len(lineas) > 2 else None
                        })
                        encontrados += 1

                print(f" Conciertos añadidos: {encontrados}")
                page += 1
                time.sleep(2)

        df = pd.DataFrame(all_concerts).drop_duplicates()
        df.to_excel("conciertos_pasados_espana.xlsx", index=False)

        print("\n Excel generado correctamente")
        print(f"Total conciertos: {len(df)}")

    except Exception as e:
        print("Error:", e)

    finally:
        input("\nPulsa Enter para cerrar el navegador...")
        driver.quit()

if __name__ == "__main__":

    main()
