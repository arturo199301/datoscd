import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 1. Hacer la petición a la página objetivo con User-Agent
url = "https://udiscover.mx/collections/cd"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

# 2. Convertir HTML con BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# 3. Localizar las tarjetas de productos
productos = soup.find_all("li", class_=lambda c: c and "grid__item" in c) or soup.find_all("div", class_=lambda c: c and "product" in c.lower())

datos = []

# 4. Extraer y limpiar títulos y precios
for prod in productos:
    titulo_elem = prod.find("a", class_=lambda c: c and "link" in c.lower()) or prod.find(["h2", "h3", "a"])
    precio_elem = prod.find("span", class_=lambda c: c and "price" in c.lower())
    
    if titulo_elem:
        titulo = titulo_elem.text.strip()
        precio_raw = precio_elem.text.strip() if precio_elem else "$0"
        
        # Extracción numérica del precio
        match_precio = re.search(r'[\d,]+(\.\d+)?', precio_raw.replace('$', '').replace('MXN', ''))
        precio_limpio = float(match_precio.group(0).replace(',', '')) if match_precio else 0.0
        
        if titulo:
            datos.append({
                "titulo": titulo,
                "precio_mxn": precio_limpio,
                "disponibilidad": "En existencia"
            })

# 5. Exportar los datos recolectados a CSV
df = pd.DataFrame(datos)
df.to_csv("catalogo_udiscover_cd.csv", index=False, encoding="utf-8-sig")
print(f"Scraping exitoso. Se extrajeron {len(df)} registros y se guardaron en 'catalogo_udiscover_cd.csv'")
