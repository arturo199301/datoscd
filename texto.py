import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://udiscover.mx/collections/cd"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, "html.parser")

# Método alternativo directo para e-commerce Shopify (JSON de productos si está presente)
res_json = requests.get("https://udiscover.mx/collections/cd/products.json")
datos = []

if res_json.status_code == 200:
    items = res_json.json().get("products", [])
    for item in items:
        precio = item.get("variants", [{}])[0].get("price", "N/A")
        datos.append({
            "titulo": item.get("title"),
            "artista_vendor": item.get("vendor"),
            "precio_mxn": f"${precio}",
            "enlace": f"https://udiscover.mx/products/{item.get('handle')}"
        })

df = pd.DataFrame(datos)
df.to_csv("udiscover_cds_catalogo.csv", index=False)
print(f"Catálogo exportado exitosamente con {len(df)} CDs a 'udiscover_cds_catalogo.csv'.")
