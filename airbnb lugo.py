# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 14:22:04 2026

@author: User
"""

import time
import os
import pandas as pd
from datetime import date, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def scrape_airbnb_prices(city, checkin, checkout, scrolls=6):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 20)

    url = f"https://www.airbnb.es/s/{city}--España/homes?checkin={checkin}&checkout={checkout}&adults=2"
    driver.get(url)

    try:
        btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar')]"))
        )
        btn.click()
        time.sleep(2)
    except:
        pass

    # Esperar resultados
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='card-container']"))
        )
    except:
        driver.save_screenshot(f"airbnb_debug_{city}_{checkin}.png")
        print(f" No se detectaron resultados para {checkin}-{checkout}")
        driver.quit()
        return []

    # Scroll
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='card-container']")
    print(f"Total de tarjetas encontradas para {checkin}-{checkout}: {len(cards)}")

    data = []

    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "div[role='group']").text.split("\n")[0]
        except:
            title = "N/A"

        price_text = "N/A"
        try:
            spans = card.find_elements(By.TAG_NAME, "span")
            for s in spans:
                if "€" in s.text:
                    price_text = s.text
                    break
        except:
            price_text = "N/A"

        try:
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = "N/A"

        data.append({
            "city": city,
            "checkin": checkin,
            "checkout": checkout,
            "title": title,
            "price": price_text,
            "link": link
        })

    driver.quit()
    return data


start_date = date(2024, 1, 5)  
end_date = date(2024, 12, 31)
delta = timedelta(days=7)       

all_data = []
city = "Lugo"

current = start_date
while current <= end_date:
    checkin = current.strftime("%Y-%m-%d")
    checkout = (current + timedelta(days=2)).strftime("%Y-%m-%d")

    print(f"\n⏳ Extrayendo datos {city}: {checkin} → {checkout}")
    week_data = scrape_airbnb_prices(city, checkin, checkout, scrolls=6)
    all_data.extend(week_data)

    current += delta

# Guardar CSV
if all_data:
    df = pd.DataFrame(all_data)
    filename = f"airbnb_{city.lower()}_prices_2024.csv"
    filepath = os.path.join(os.getcwd(), filename)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print("\n CSV guardado:", filepath)
else:
    print(f" No se extrajeron datos para {city} en 2024.")
