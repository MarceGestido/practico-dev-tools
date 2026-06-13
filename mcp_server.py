import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PARENT_PAGE_ID = os.environ.get("NOTION_PARENT_PAGE_ID", "b5ef2741d4424fe2bceda6edc28a09ae")

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

mcp = FastMCP("fmcp_udhfg8cHvMjuO3VdpBCXfkozwEHwvp_icQUR0rg54wg")


@mcp.tool()
def listar_paginas() -> str:
    """Lista todas las páginas disponibles en Notion."""
    response = requests.post(
        "https://api.notion.com/v1/search",
        headers=NOTION_HEADERS,
        json={"filter": {"value": "page", "property": "object"}},
    )
    if response.status_code != 200:
        return f"Error {response.status_code}: {response.json()}"

    results = response.json().get("results", [])
    if not results:
        return "No se encontraron páginas."

    lineas = [f"Se encontraron {len(results)} páginas:\n"]
    for page in results:
        title_parts = page.get("properties", {}).get("title", {}).get("title", [])
        title = title_parts[0]["text"]["content"] if title_parts else "Sin título"
        lineas.append(f"- {title} | ID: {page['id']} | URL: {page['url']}")
    return "\n".join(lineas)


@mcp.tool()
def crear_pagina(titulo: str, contenido: str) -> str:
    """Crea una nueva página en Notion con el título y contenido indicados."""
    payload = {
        "parent": {"database_id": PARENT_PAGE_ID},
        "properties": {
            "title": {"title": [{"text": {"content": titulo}}]}
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": contenido}}]
                },
            }
        ],
    }
    response = requests.post(
        "https://api.notion.com/v1/pages", headers=NOTION_HEADERS, json=payload
    )
    if response.status_code == 200:
        page = response.json()
        return f"Página creada exitosamente!\nID: {page['id']}\nURL: {page['url']}"
    return f"Error {response.status_code}: {response.json()}"


if __name__ == "__main__":
    mcp.run()
