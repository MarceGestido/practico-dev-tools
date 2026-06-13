import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.notion.com/v1/search",
    headers=headers,
    json={"filter": {"value": "page", "property": "object"}}
)

if response.status_code == 200:
    results = response.json().get("results", [])
    print(f"Se encontraron {len(results)} páginas:\n")
    for page in results:
        title_parts = page.get("properties", {}).get("title", {}).get("title", [])
        title = title_parts[0]["text"]["content"] if title_parts else "Sin título"
        print(f"- {title} | ID: {page['id']} | URL: {page['url']}")
else:
    print(f"Error {response.status_code}: {response.json()}")
