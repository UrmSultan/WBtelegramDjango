from api.session import get_session

async def get_supplier_name(token: str) -> str:
    url = " https://common-api.wildberries.ru/api/v1/seller-info"
    headers = {"Authorization": f"Bearer {token}"}

    session = await get_session()
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("name", "Без имени")
        print(f"⚠ Ошибка {response.status} при запросе seller-info")
        return "Без имени"