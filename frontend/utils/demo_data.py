"""Backend 없이 공개 데모를 실행하기 위한 읽기 전용 데이터 로더."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[2] / "database" / "common" / "data" / "processed"


def _read(name: str):
    with (DATA_DIR / name).open(encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def _dataset():
    pokemon = _read("pokemon.json")
    types = {row["id"]: row["name"] for row in _read("types.json")}
    abilities = {row["id"]: row for row in _read("abilities.json")}
    species = {row["id"]: row for row in _read("species.json")}

    descriptions = {}
    versions = {}
    for row in _read("flavor_text.json"):
        species_id = row["species_id"]
        descriptions.setdefault(species_id, row["content"])
        versions.setdefault(species_id, []).append(row["version_name"])

    type_rows: dict[int, list[dict]] = {}
    for row in _read("pokemon_types.json"):
        type_rows.setdefault(row["pokemon_id"], []).append(
            {
                "slot": row["slot"],
                "type_": {"id": row["type_id"], "name": types[row["type_id"]]},
            }
        )

    ability_rows: dict[int, list[dict]] = {}
    for row in _read("pokemon_abilities.json"):
        ability = abilities.get(row["ability_id"])
        if ability:
            ability_rows.setdefault(row["pokemon_id"], []).append(
                {
                    "slot": row["slot"],
                    "is_hidden": row["is_hidden"],
                    "ability": ability,
                }
            )

    items = []
    for row in pokemon:
        item = dict(row)
        species_id = row.get("species_id") or row["id"]
        species_row = species.get(species_id, {})
        item["types"] = sorted(type_rows.get(row["id"], []), key=lambda value: value["slot"])
        item["abilities"] = sorted(ability_rows.get(row["id"], []), key=lambda value: value["slot"])
        item["classification"] = species_row.get("classification")
        item["description"] = descriptions.get(species_id)
        item["game_versions"] = list(dict.fromkeys(versions.get(species_id, [])))
        items.append(item)

    return items


def ability_names() -> list[str]:
    return sorted({row["name"] for row in _read("abilities.json")})


def pokemon_list(
    *,
    limit: int = 50,
    search: str | None = None,
    ability: str | None = None,
    min_id: int = 1,
    max_id: int = 1025,
    types: list[str] | None = None,
) -> dict:
    query = (search or "").strip().lower()
    selected_types = set(types or [])
    filtered = []

    for item in _dataset():
        species_id = item.get("species_id") or item["id"]
        if not min_id <= species_id <= max_id:
            continue

        item_types = {row["type_"]["name"] for row in item["types"]}
        if selected_types and not selected_types.issubset(item_types):
            continue

        item_abilities = {row["ability"]["name"] for row in item["abilities"]}
        if ability and ability not in item_abilities:
            continue

        searchable = " ".join([item.get("name", ""), *item_types, *item_abilities]).lower()
        if query and query not in searchable:
            continue
        filtered.append(item)

    return {"items": filtered[:limit], "total": len(filtered)}


def pokemon_detail(pokemon_id: int) -> dict | None:
    return next((item for item in _dataset() if item["id"] == pokemon_id), None)

