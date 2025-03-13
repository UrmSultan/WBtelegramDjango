import aiohttp

async def get_wb_products(token: str):
    url = "https://content-api.wildberries.ru/content/v2/get/cards/list"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "settings": {
            "cursor": {"limit": 100},
            "filter": {}
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url,headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("cards", [])
            return []

async def get_all_products(token: str):
    url = "https://content-api.wildberries.ru/content/v2/get/cards/list"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    all_products = []
    next_cursor = None

    while True:
        payload = {
            "settings": {
                "cursor": {"limit": 100},
                "filter": {}
            }
        }
        if next_cursor:
            payload["settings"]["cursor"]["next"] = next_cursor

        async with aiohttp.ClientSession() as session:
            async with session.post(url,headers=headers, json=payload) as response:
                if response.status != 200:
                    print(f"Ошибка {response.status}: {await response.text()}")
                    break

                data = await response.json()
                cards = data.get("cards", [])
                if not cards:
                    break

                all_products.extend(cards)

                new_cursor = data.get("cursor",None)

                if not new_cursor or new_cursor == next_cursor:
                    break

                next_cursor = new_cursor

    return all_products