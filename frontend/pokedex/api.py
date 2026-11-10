import os
import requests
import streamlit as st

from pokedex.constants import TYPE_ORDER, _ICON_FILENAME_OVERRIDE
from utils.demo_data import ability_names, pokemon_detail, pokemon_list

BACKEND_URL = os.environ.get("BACKEND_URL") or os.environ.get("BACKEND_API_URL") or "http://localhost:8000"
API_V1_STR = "/api/v1/pokemon"


@st.cache_data(show_spinner=False)
def fetch_abilities():
    try:
        resp = requests.get(f"{BACKEND_URL}{API_V1_STR}/abilities", timeout=3)
        if resp.status_code == 200:
            return ["전체"] + sorted(resp.json())
    except Exception:
        pass
    return ["전체"] + ability_names()


def fetch_pokemon(params):
    """운영 API를 우선 사용하고, 연결할 수 없으면 저장소 JSON으로 전환한다."""
    try:
        response = requests.get(f"{BACKEND_URL}{API_V1_STR}/", params=params, timeout=5)
        if response.ok:
            return response.json(), False
    except requests.RequestException:
        pass

    data = pokemon_list(
        limit=params.get("limit", 50),
        search=params.get("search"),
        ability=params.get("ability"),
        min_id=params.get("min_id", 1),
        max_id=params.get("max_id", 1025),
        types=params.get("types"),
    )
    return data, True


def fetch_pokemon_detail(pokemon_id):
    try:
        response = requests.get(f"{BACKEND_URL}{API_V1_STR}/{pokemon_id}", timeout=5)
        if response.ok:
            return response.json(), False
    except requests.RequestException:
        pass
    return pokemon_detail(pokemon_id), True


@st.cache_data
def load_type_icons():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_dir = os.path.join(base_path, "img", "type")
    icons = {}
    for ko, _ in TYPE_ORDER:
        filename = _ICON_FILENAME_OVERRIDE.get(ko, ko)
        path = os.path.join(icon_dir, f"{filename}.svg")
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    icons[ko] = f.read()
            else:
                icons[ko] = ""
        except Exception:
            icons[ko] = ""
    return icons
