#!/usr/bin/env python3
"""
Script para criar subitens do ML Sales Forecasting no Notion usando requests puro.
"""

import os
import json

# IDs do Notion  
DATABASE_ID = "1fa962a7693c80deb90beaa513dcf9d1"
PARENT_CARD_ID = "296962a7693c81bdba7fda10d3b0ff06"

SUBITENS = [
    {
        "title": "Fase 1: Notebooks ML - Analise e Modelagem",
        "status": "Concluido",
        "priority": "Alta",
        "start": "2025-10-27",
        "end": "2025-10-28",
    },
    {
        "title": "Fase 2: API Backend FastAPI",
        "status": "Concluido",
        "priority": "Alta",
        "start": "2025-10-28",
        "end": "2025-10-29",
    },
    {
        "title": "Fase 3: Docker & Infraestrutura",
        "status": "Concluido",
        "priority": "Alta",
        "start": "2025-10-29",
        "end": "2025-10-29",
    },
    {
        "title": "Fase 4: Testes Automatizados",
        "status": "Concluido",
        "priority": "Alta",
        "start": "2025-10-29",
        "end": "2025-10-29",
    },
    {
        "title": "Fase 5: Frontend React",
        "status": "Concluido",
        "priority": "Alta",
        "start": "2025-10-29",
        "end": "2025-10-29",
    },
    {
        "title": "Fase 6: Documentacao Final",
        "status": "Concluido",
        "priority": "Alta",
        "start": "2025-10-29",
        "end": "2025-10-29",
    },
]


def criar_curl_command(subitem):
    """Gera comando curl para criar página no Notion."""
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Project name": {
                "title": [
                    {"text": {"content": subitem["title"]}}
                ]
            },
            "Status": {
                "select": {"name": subitem["status"]}
            },
            "Prioridade": {
                "select": {"name": subitem["priority"]}
            },
            "Parent item": {
                "relation": [{"id": PARENT_CARD_ID}]
            },
            "Período": {
                "date": {
                    "start": subitem["start"],
                    "end": subitem.get("end")
                }
            }
        }
    }
    
    json_data = json.dumps(payload, indent=2)
    
    return f"""curl -X POST https://api.notion.com/v1/pages \\
  -H "Authorization: Bearer $NOTION_TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "Notion-Version: 2022-06-28" \\
  -d '{json_data}'
"""


def main():
    print("=" * 70)
    print("Gerando comandos CURL para criar subitens no Notion")
    print("=" * 70)
    print()
    
    print("Execute os seguintes comandos no terminal:")
    print()
    
    for i, subitem in enumerate(SUBITENS, 1):
        print(f"# [{i}/{len(SUBITENS)}] {subitem['title']}")
        print(criar_curl_command(subitem))
        print()


if __name__ == "__main__":
    main()

