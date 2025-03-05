import aiohttp

async def get_wb_products(token: str):
    url = "https://content-api.wildberries.ru/content/v2/get/cards/list"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "settings": {
            "cursor": {"limit": 10},
            "filter": {}
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("cards", [])
            return []