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

def format_date(timestamp):
    if not timestamp:
        return None
    dt = datetime.fromtimestamp(timestamp / 1000)
    return dt.strftime("%d/%m/%Y")

def get_character_profile(name, token, locale):
    base_url = f"https://{REGION}.api.blizzard.com/profile/wow/character/{REALM.lower()}/{name.lower()}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"namespace": NAMESPACE, "locale": locale}

    try:
        profile = requests.get(base_url, headers=headers, params=params).json()
        media = requests.get(f"{base_url}/character-media", headers=headers, params=params).json()
        equipment = requests.get(f"{base_url}/equipment", headers=headers, params=params).json()

        img_url = None
        for asset in media.get("assets", []):
            if asset.get("key") == "main":
                img_url = asset.get("value")
                break

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
            "media": img_url,
            "equipped_item_level": equipment.get("equipped_item_level"),
            "average_item_level": profile.get("average_item_level"),
            "guild": profile.get("guild", {}).get("name"),
            "achievement_points": profile.get("achievement_points"),
            "last_login": format_date(profile.get("last_login_timestamp")),
        }

    except Exception as e:
        print(f"Erro ao buscar {name} ({locale}): {e}")
        return None

def fetch_and_save(locale, filename):
    token = get_access_token()
    results = []

    for name in CHARACTERS:
        data = get_character_profile(name, token, locale)
        if data:
            results.append(data)
        sleep(1)

    with open(f"data/{filename
