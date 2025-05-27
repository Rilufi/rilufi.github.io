import os
import json
import requests
from datetime import datetime

# Configurações principais
REGION = "us"
REALM = "stormrage"
NAMESPACE = f"profile-{REGION}"
LOCALES = {"en": "en_US", "pt": "pt_BR"}
CHARACTERS = [
    "Rilufi", "Draconyrith", "Kunglufi", "Thulduk", "Rotpelt",
    "Rilufix", "Shamil", "Lythendre", "Zarknall", "Rilufito"
]

def get_token(client_id, client_secret):
    url = f"https://{REGION}.battle.net/oauth/token"
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    return response.json()["access_token"]

def get_character_profile(name, token, locale="en_US"):
    base_url = f"https://{REGION}.api.blizzard.com/profile/wow/character/{REALM}/{name.lower()}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"namespace": NAMESPACE, "locale": locale}

    profile = requests.get(base_url, headers=headers, params=params).json()
    media_data = requests.get(f"{base_url}/character-media", headers=headers, params=params).json()

    media_url = None
    if "assets" in media_data:
        for asset in media_data["assets"]:
            if asset.get("key") in ["main", "render", "avatar"]:
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

def save_data(locale_code, token):
    locale = LOCALES[locale_code]
    characters = [
        get_character_profile(name, token, locale)
        for name in CHARACTERS
    ]
    characters.sort(key=lambda c: c["average_item_level"] or 0, reverse=True)
    with open(f"data/wow{'_pt' if locale_code == 'pt' else ''}.json", "w", encoding="utf-8") as f:
        json.dump(characters, f, indent=2, ensure_ascii=False)

def main():
    client_id = os.getenv("BLIZZARD_CLIENT_ID")
    client_secret = os.getenv("BLIZZARD_CLIENT_SECRET")
    token = get_token(client_id, client_secret)
    save_data("en", token)
    save_data("pt", token)

if __name__ == "__main__":
    main()
