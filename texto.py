import requests
import pandas as pd

# 1. Endpoint JSON directo de la colección de Shopify
url = "https://udiscover.mx/collections/cd/products.json?limit=250"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

datos = []

if response.status_code == 200:
    data = response.json()
    productos = data.get("products", [])
    
    for prod in productos:
        titulo = prod.get("title", "").strip()
        
        # Analizar variantes para precio y disponibilidad
        variants = prod.get("variants", [])
        if variants:
            # Tomar la primera variante (o la principal)
            primera_variante = variants[0]
            precio = float(primera_variante.get("price", 0.0))
            disponible = primera_variante.get("available", False)
            disponibilidad = "En existencia" if disponible else "Agotado"
        else:
            precio = 0.0
            disponibilidad = "Agotado"
            
        datos.append({
            "titulo": titulo,
            "precio_mxn": precio,
            "disponibilidad": disponibilidad
        })

# 2. Exportar a CSV
df = pd.DataFrame(datos)
df.to_csv("catalogo_udiscover_cd.csv", index=False, encoding="utf-8-sig")

print(f"Éxito: Se extrajeron {len(df)} productos con precio y disponibilidad reales.")
print(df.head())
