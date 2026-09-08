import requests
import pandas as pd

# URL de la página principal de la colección en uDiscover Store México
url = "https://udiscover.mx/collections/cd/products.json"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# Realizar la petición
response = requests.get(url, headers=headers)

datos = []

if response.status_code == 200:
    data = response.json()
    # Contiene únicamente los productos cargados en el render principal
    productos = data.get("products", [])
    
    for prod in productos:
        titulo = prod.get("title", "").strip()
        variants = prod.get("variants", [])
        
        if variants:
            variante_principal = variants[0]
            precio = float(variante_principal.get("price", 0.0))
            disponible = variante_principal.get("available", False)
            disponibilidad = "En existencia" if disponible else "Agotado"
        else:
            precio = 0.0
            disponibilidad = "Agotado"
            
        datos.append({
            "titulo": titulo,
            "precio_mxn": precio,
            "disponibilidad": disponibilidad
        })

# Crear el DataFrame con los productos de la primera página
df = pd.DataFrame(datos)

# Guardar a CSV
df.to_csv("catalogo_principal_udiscover.csv", index=False, encoding="utf-8-sig")

print(f"Se extrajeron {len(df)} productos de la página principal.")
print(df)
