import os
import requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PARENT_PAGE_ID = os.environ.get("NOTION_PARENT_PAGE_ID", "b5ef2741d4424fe2bceda6edc28a09ae")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

payload = {
    "parent": {"database_id": PARENT_PAGE_ID},
    "properties": {
        "title": {
            "title": [{"text": {"content": "Página creada desde VS Code con MCP"}}]
        }
    },
    "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": "Esta página fue creada desde VS Code usando el MCP server de Notion y Python."}}]
            }
        }
    ]
}

response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)

if response.status_code == 200:
    page = response.json()
    print(f"Página creada exitosamente!")
    print(f"ID: {page['id']}")
    print(f"URL: {page['url']}")
else:
    print(f"Error {response.status_code}: {response.json()}")
