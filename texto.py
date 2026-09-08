import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 1. Hacer la petición a uDiscover Store México
url = "https://udiscover.mx/collections/cd"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

# 2. Parsear el documento HTML
soup = BeautifulSoup(response.text, "html.parser")

# 3. Localizar las tarjetas de producto (Shopify Grid)
productos = soup.find_all("li", class_=lambda c: c and "grid__item" in c) or soup.find_all("div", class_=lambda c: c and "product" in c.lower())

datos = []

# 4. Procesar cada producto
for prod in productos:
    # --- Extracción de Título ---
    titulo_elem = prod.find("a", class_=lambda c: c and "link" in c.lower()) or prod.find(["h2", "h3", "a"])
    if not titulo_elem:
        continue
    
    titulo = titulo_elem.text.strip()
    if not titulo:
        continue

    # --- Extracción y Determinación de Disponibilidad ---
    prod_text = prod.text.lower()
    prod_html = str(prod).lower()
    
    # Comprobar indicadores de "Agotado" en badges, clases o texto
    es_agotado = (
        "sold-out" in prod_html or 
        "sold_out" in prod_html or 
        "agotado" in prod_text or 
        "out-of-stock" in prod_html or
        bool(prod.find(class_=lambda c: c and "sold-out" in c.lower()))
    )
    disponibilidad = "Agotado" if es_agotado else "En existencia"

    # --- Extracción de Precio ---
    # Priorizar precio de oferta si existe; de lo contrario, tomar precio regular
    precio_elem = (
        prod.find("span", class_=lambda c: c and ("price-item--sale" in c or "price-item--last" in c)) or
        prod.find("span", class_=lambda c: c and "price-item" in c) or
        prod.find("span", class_=lambda c: c and "price" in c.lower())
    )
    
    precio_limpio = 0.0
    if precio_elem:
        precio_raw = precio_elem.text.strip()
        # Buscar el valor numérico en el texto extraído
        match_precio = re.search(r'[\d,]+(\.\d+)?', precio_raw.replace('$', '').replace('MXN', ''))
        if match_precio:
            precio_limpio = float(match_precio.group(0).replace(',', ''))

    datos.append({
        "titulo": titulo,
        "precio_mxn": precio_limpio,
        "disponibilidad": disponibilidad
    })

# 5. Exportar a CSV
df = pd.DataFrame(datos)
df.to_csv("catalogo_udiscover_cd.csv", index=False, encoding="utf-8-sig")

print(f"Scraping finalizado. Se extrajeron {len(df)} registros correctamente.")
