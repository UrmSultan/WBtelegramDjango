def parse_characteristic(product: dict, characteristic_name: str) -> str:
    char_list = product.get("characteristics", [])
    for char in char_list:
        if char.get("name") == characteristic_name:
            values = char.get("value", [])
            return ", ".join(values) if values else "N/A"
    return "N/A"