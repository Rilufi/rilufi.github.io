import os
import requests
import json
from time import sleep

CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")
REGION = "us"
REALM = "stormrage"
LOCALE = "en_US"
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

def get_character_profile(name, token):
    base_url = f"https://{REGION}.api.blizzard.com/profile/wow/character/{REALM.lower()}/{name.lower()}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"namespace": NAMESPACE, "locale": LOCALE}

    profile = requests.get(base_url, headers=headers, params=params).json()
    media = requests.get(f"{base_url}/character-media", headers=headers, params=params).json()
    equipment = requests.get(f"{base_url}/equipment", headers=headers, params=params).json()

    return {
        "name": profile.get("name"),
        "realm": profile.get("realm", {}).get("name"),
        "level": profile.get("level"),
        "race": profile.get("race", {}).get("name"),
        "class": profile.get("character_class", {}).get("name"),
        "spec": profile.get("active_spec", {}).get("name", ""),
        "faction": profile.get("faction", {}).get("name"),
        "gender": profile.get("gender", {}).get("name"),
        "media": media.get("assets", [{}])[0].get("value"),
        "equipped_item_level": equipment.get("equipped_item_level")
    }

def main():
    token = get_access_token()
    all_data = []

    for name in CHARACTERS:
        try:
            data = get_character_profile(name, token)
            all_data.append(data)
            sleep(1)  # Evita rate limiting
        except Exception as e:
            print(f"Erro ao buscar {name}: {e}")

    with open("data/wow.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    LOCALE = "pt_BR"
    
    for name in CHARACTERS:
        try:
            data = get_character_profile(name, token)
            all_data.append(data)
            sleep(1)  # Evita rate limiting
        except Exception as e:
            print(f"Erro ao buscar {name}: {e}")

    with open("data/wow_pt.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
