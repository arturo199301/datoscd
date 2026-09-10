mport requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://udiscover.mx/collections/cd"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Método directo para e-commerce Shopify
res_json = requests.get("https://udiscover.mx/collections/cd/products.json", headers=headers)
datos = []

if res_json.status_code == 200:
    items = res_json.json().get("products", [])
    for item in items:
        precio = item.get("variants", [{}])[0].get("price", "N/A")
        datos.append({
            "producto": item.get("title"),
            "artista": item.get("vendor"),
            "precio_mxn": f"${precio}"
        })

df = pd.DataFrame(datos)
df.to_csv("udiscover_cds_catalogo.csv", index=False)
print(f"Catálogo exportado exitosamente con {len(df)} CDs a 'udiscover_cds_catalogo.csv'.")
