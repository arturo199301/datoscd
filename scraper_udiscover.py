import requests
from bs4 import BeautifulSoup
import pandas as pd

# Script completo adaptado para uDiscover Store México
url = "https://udiscover.mx/collections/cd"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, "html.parser")
productos = soup.find_all("div", class_=lambda c: c and ("product" in c.lower() or "grid__item" in c.lower()))

datos = []
for prod in productos:
    titulo_elem = prod.find(["a", "h3", "h2"], class_=lambda c: c and ("title" in c.lower() or "heading" in c.lower()))
    precio_elem = prod.find(["span", "p", "div"], class_=lambda c: c and "price" in c.lower())

    if titulo_elem and precio_elem:
        titulo = titulo_elem.text.strip()
        precio_raw = precio_elem.text.strip()
        precio = float(precio_raw.replace("$", "").replace(",", "").replace("MXN", "").strip() or 0)

        datos.append({
            "titulo": titulo,
            "precio_mxn": precio,
            "disponibilidad": "En existencia"
        })

df = pd.DataFrame(datos)
df.to_csv("catalogo_udiscover_cd.csv", index=False, encoding="utf-8-sig")
print("Scraping exitoso y archivo catalogo_udiscover_cd.csv creado.")
