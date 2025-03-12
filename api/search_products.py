import aiohttp
import logging


async def search_wb_products(token:str, query: str, limit=100):
    url = "https://content-api.wildberries.ru/content/v2/get/cards/list"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "settings": {
            "sort": {
                "ascending": False
            },
            "filter": {
                "textSearch": query,         # Insert user’s query
                "allowedCategoriesOnly": False,
            },
            "cursor": {
                "limit": limit
            }
        }
    }

    logging.info(f"🔍 Searching for: {query}, Limit: {limit}")
    logging.info(f"📡 Request payload: {payload}")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            status = response.status
            logging.info(f"🔄 Response Status: {status}")

            if status == 200:
                data = await response.json()
                return data.get("cards", [])
            else:
                print(f"❌ Ошибка {response.status}: {await response.text()}")
                return []