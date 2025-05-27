import os
import requests
import json
from time import sleep

REGION = "us"
NAMESPACE = "profile-us"
REALM = "stormrage"
CHARACTERS = [
    "Rilufi",
    "Draconyrith",
    "Kunglufi",
    "Thulduk",
    "Rotpelt",
    "Rilufix",
    "Shamil",
    "Lythendre",
    "Zarknall",
    "Rilufito"
]

CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")

def get_access_token():
    url = f"https://{REGION}.battle.net/oauth/token"
    data = {"grant_type": "client_credentials"}
    resp = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    resp.raise_for_status()
    return resp.json()["access_token"]

def get_character_profile(name, token, locale="en_US"):
    base_url = f"https://{REGION}.api.blizzard.com/profile/wow/character/{REALM}/{name.lower()}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"namespace": NAMESPACE, "locale": locale}

    profile = requests.get(base_url, headers=headers, params=params).json()
    media_data = requests.get(f"{base_url}/character-media", headers=headers, params=params).json()

    media_url = None
    for asset in media_data.get("assets", []):
        if asset.get("key") == "main":
            media_url = asset.get("value")
            break

    return {
        "name": profile.get("name"),
        "realm": profile.get("realm", {}).get("name"),
        "level": profile.get("level"),
        "race": profile.get("race", {}).get("name"),
        "class": profile.get("character_class", {}).get("name"),
        "spec": profile.get("active_spec", {}).get("name") if profile.get("active_spec") else "",
        "faction": profile.get("faction", {}).get("name"),
        "gender": profile.get("gender", {}).get("name"),
        "media": media_url,
        "equipped_item_level": profile.get("equipped_item_level"),
        "average_item_level": profile.get("average_item_level"),
        "guild": profile.get("guild", {}).get("name") if profile.get("guild") else None,
        "achievement_points": profile.get("achievement_points"),
    }

def save_characters(locale, filename):
    token = get_access_token()
    data = []

    for name in CHARACTERS:
        try:
            print(f"Buscando {name} ({locale})...")
            char_data = get_character_profile(name, token, locale)
            data.append(char_data)
            sleep(1)
        except Exception as e:
            print(f"Erro com {name}: {e}")

    # Ordenar pelo average_item_level decrescente
    data.sort(key=lambda c: c.get("average_item_level") or 0, reverse=True)

    os.makedirs("data", exist_ok=True)
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Salvo em data/{filename}")

if __name__ == "__main__":
    save_characters("en_US", "wow.json")
    save_characters("pt_BR", "wow_pt.json")
