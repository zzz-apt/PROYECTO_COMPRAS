import requests
import json

# URL de la API de Geonode para proxies de Venezuela
API_URL = "https://proxylist.geonode.com/api/proxy-list?country=VE&limit=500&page=1&sort_by=lastChecked&sort_type=desc"

# 1. Hacer la solicitud HTTP GET
response = requests.get(API_URL)
response.raise_for_status() # Lanza una excepción para códigos de error (4xx o 5xx)

# 2. Convertir la respuesta a JSON (Python dictionary/list)
datos_json = response.json()

# 3. Acceder a la lista principal de proxies (que está bajo la clave 'data')
# Si la API cambia, puede que esta clave necesite ajustarse.
lista_proxies = datos_json.get("data", [])


# --- Solución con Comprensión de Lista y f-string ---
# Usamos un f-string para formatear la cadena en cada iteración.
proxys = [
    f"https://{item['ip']}:{item['port']}" 
    for item in lista_proxies
]

