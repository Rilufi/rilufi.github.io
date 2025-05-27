import os
import requests
import json
from time import sleep
from datetime import datetime

CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")
REGION = "us"
REALM = "stormrage"
NAMESPACE = "profile-us"

CHARACTERS = [
    "Rilufi", "Draconyrith", "Kunglufi", "Thulduk", "Rotpelt",
    "Rilufix", "Shamil", "Lythendre", "Zarknall", "Rilufito"
]

def get_access_token():
    response = requests.post(
        f"https://{REGION}.battle.net/oauth/token",
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={"grant_type": "client_credentials"}
    )
    response.raise_for_status()
    return response.json()["access_token"]

def get_character_profile(name, token, locale):
    base_url = f"https://{REGION}.api.blizzard.com/profile/wow/character/{REALM.lower()}/{name.lower()}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"namespace": NAMESPACE, "locale": locale}

    profile = requests.get(base_url, headers=headers, params=params).json()
    media = requests.get(f"{base_url}/character-media", headers=headers, params=params).json()
    equipment = requests.get(f"{base_url}/equipment", headers=headers, params=params).json()

    return {
        "name": profile.get("name"),
        "title": profile.get("active_title", {}).get("name"),
        "realm": profile.get("realm", {}).get("name"),
        "level": profile.get("level"),
        "race": profile.get("race", {}).get("name"),
        "class": profile.get("character_class", {}).get("name"),
        "spec": profile.get("active_spec", {}).get("name", ""),
        "faction": profile.get("faction", {}).get("name"),
        "gender": profile.get("gender", {}).get("name"),
        "media": next((a.get("value") for a in media.get("assets", []) if a.get("key") == "main"), None),
        "equipped_item_level": equipment.get("equipped_item_level"),
        "average_item_level": equipment.get("average_item_level"),
        "guild": profile.get("guild", {}).get("name"),
        "achievement_points": profile.get("achievement_points"),
        "last_login": datetime.utcfromtimestamp(
            profile.get("last_login_timestamp", 0) / 1000
        ).strftime("%d/%m/%Y") if profile.get("last_login_timestamp") else None
    }

def save_characters(locale, filename, token):
    print(f"Coletando dados em {locale}...")
    characters_data = []

    for name in CHARACTERS:
        try:
            data = get_character_profile(name, token, locale)
            characters_data.append(data)
            sleep(1)  # evita rate limit
        except Exception as e:
            print(f"Erro ao buscar {name}: {e}")

    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(characters_data, f, ensure_ascii=False, indent=2)

def main():
    token = get_access_token()
    save_characters("en_US", "wow.json", token)
    save_characters("pt_BR", "wow_pt.json", token)

if __name__ == "__main__":
    main()
