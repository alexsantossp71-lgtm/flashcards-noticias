import requests
import json

url = "http://localhost:8000/api/generate-content"
payload = {
    "headline": "Consumo de adoçante pode estar relacionado a demência, mostra estudo brasileiro",
    "url": "https://iclnoticias.com.br/estudo-brasileiro-inedito/",
    "source": "ICL Notícias",
    "stylePrompt": "estilo vetorial moderno"
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    with open("latest_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
