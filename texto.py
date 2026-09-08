import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://udiscover.mx/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, "html.parser")
productos = soup.find_all("li", class_=lambda c: c and "grid__item" in c) or soup.find_all("div", class_=lambda c: c and "product" in c.lower())

datos = []
for prod in productos:
    titulo_elem = prod.find("a", class_=lambda c: c and "link" in c.lower()) or prod.find(["h2", "h3", "a"])
    precio_elem = prod.find("span", class_=lambda c: c and "price" in c.lower())
    
    if titulo_elem:
        titulo = titulo_elem.text.strip()
        precio_raw = precio_elem.text.strip() if precio_elem else "$0"
        
        match_precio = re.search(r'[\d,]+(\.\d+)?', precio_raw.replace('$', '').replace('MXN', ''))
        precio_limpio = float(match_precio.group(0).replace(',', '')) if match_precio else 0.0
        
        prod_html = str(prod).lower()
        prod_text = prod.text.lower()
        es_agotado = "sold-out" in prod_html or "agotado" in prod_text or "sold_out" in prod_html
        disponibilidad = "Agotado" if es_agotado else "En existencia"
        
        if titulo:
            datos.append({
                "titulo": titulo,
                "precio_mxn": precio_limpio,
                "disponibilidad": disponibilidad
            })

df = pd.DataFrame(datos)
df.to_csv("catalogo_home_udiscover.csv", index=False, encoding="utf-8-sig")
print(f"Scraping exitoso. Se extrajeron {len(df)} registros dinámicamente de la página principal y se guardaron en catalogo_home_udiscover.csv")
