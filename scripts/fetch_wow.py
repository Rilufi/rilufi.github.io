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
raider_key = os.getenv("RAIDER_IO_API_KEY")

def get_token(client_id, client_secret):
    """Obtém token de acesso da API Blizzard"""
    url = f"https://{REGION}.battle.net/oauth/token"
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()["access_token"]

def get_character_media(name, token, locale="en_US"):
    """Obtém URLs de mídia do personagem em diferentes qualidades"""
    url = f"https://{REGION}.api.blizzard.com/profile/wow/character/{REALM}/{name.lower()}/character-media"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"namespace": NAMESPACE, "locale": locale}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        media_data = response.json()
        
        # Prioridade: main-raw > main > avatar
        media_url = None
        if "assets" in media_data:
            for asset in media_data["assets"]:
                if asset.get("key") == "main-raw":
                    return asset["value"]  # Retorna imediatamente a melhor qualidade
                elif asset.get("key") == "main" and not media_url:
                    media_url = asset["value"]
                elif asset.get("key") == "avatar" and not media_url:
                    media_url = asset["value"]
        
        return media_url
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter mídia para {name}: {e}")
        return None

def get_raider_io_data(name, realm=REALM, region=REGION):
    """Obtém dados do Raider.IO para personagem"""
    url = f"https://raider.io/api/v1/characters/profile"
    params = {
        "region": region,
        "realm": realm.lower(),
        "name": name.lower(),
        "fields": "mythic_plus_scores,mythic_plus_best_runs,mythic_plus_alternate_runs"
    }
    headers = {"Authorization": f"Bearer {raider_key}"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados do Raider.IO para {name}: {e}")
        return None

def get_character_profile(name, token, locale="en_US"):
    """Obtém dados completos do personagem"""
    base_url = f"https://{REGION}.api.blizzard.com/profile/wow/character/{REALM}/{name.lower()}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"namespace": NAMESPACE, "locale": locale}

    try:
        # Obtém perfil básico
        profile_response = requests.get(base_url, headers=headers, params=params)
        profile_response.raise_for_status()
        profile = profile_response.json()

        # Obtém mídia
        media_url = get_character_media(name, token, locale)

        # Obtém equipamentos
        equipment_response = requests.get(f"{base_url}/equipment", headers=headers, params=params)
        equipment_data = equipment_response.json() if equipment_response.status_code == 200 else {}

        # Obtém dados do Raider.IO
        rio_data = get_raider_io_data(name)
        
        # Processa dados do Mythic+
        mythic_plus = {}
        if rio_data:
            mythic_plus = {
                "score": rio_data.get("mythic_plus_scores", {}).get("all"),
                "best_runs": rio_data.get("mythic_plus_best_runs", []),
                "alternate_runs": rio_data.get("mythic_plus_alternate_runs", []),
                "season": rio_data.get("mythic_plus_season")
            }

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
            "media_main": media_url,
            "media_main_raw": media_url,
            "equipped_item_level": profile.get("equipped_item_level"),
            "average_item_level": profile.get("average_item_level"),
            "guild": profile.get("guild", {}).get("name") if profile.get("guild") else None,
            "achievement_points": profile.get("achievement_points"),
            "mythic_plus": mythic_plus if mythic_plus.get("score") else None,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter perfil para {name}: {e}")
        return None

def save_data(locale_code, token):
    """Salva dados dos personagens em arquivo JSON"""
    locale = LOCALES[locale_code]
    characters = []
    
    for name in CHARACTERS:
        char_data = get_character_profile(name, token, locale)
        if char_data:
            characters.append(char_data)
    
    # Ordena por item level (maior primeiro)
    characters.sort(key=lambda c: c["average_item_level"] or 0, reverse=True)
    
    filename = f"data/wow{'_pt' if locale_code == 'pt' else ''}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(characters, f, indent=2, ensure_ascii=False)
    print(f"Dados salvos em {filename}")

def main():
    """Função principal"""
    try:
        client_id = os.getenv("BLIZZARD_CLIENT_ID")
        client_secret = os.getenv("BLIZZARD_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("BLIZZARD_CLIENT_ID e BLIZZARD_CLIENT_SECRET devem estar definidos")
        
        token = get_token(client_id, client_secret)
        save_data("en", token)
        save_data("pt", token)
    except Exception as e:
        print(f"Erro durante execução: {e}")

if __name__ == "__main__":
    main()
