"""OpenDocument Text export routes."""

from fastapi import APIRouter
from fastapi.responses import Response

from ..repositories import character_classes, monsters, spells
from ..services.odt import (
    ODT_MIMETYPE,
    export_character_classes,
    export_monsters,
    export_spells,
)

router = APIRouter(prefix="/api/export", tags=["exports"])


@router.get("/monsters")
def export_monster_profiles(sort: str = "Name") -> Response:
    payload = export_monsters(monsters.list_monsters(sort))
    return Response(
        content=payload,
        media_type=ODT_MIMETYPE,
        headers={"Content-Disposition": 'attachment; filename="monsters.odt"'},
    )


@router.get("/spells")
def export_spell_profiles(sort: str = "Name") -> Response:
    payload = export_spells(spells.list_spells(sort))
    return Response(
        content=payload,
        media_type=ODT_MIMETYPE,
        headers={"Content-Disposition": 'attachment; filename="spells.odt"'},
    )


@router.get("/character-classes")
def export_character_class_profiles(sort: str = "Name") -> Response:
    payload = export_character_classes(
        character_classes.list_character_classes(sort)
    )
    return Response(
        content=payload,
        media_type=ODT_MIMETYPE,
        headers={
            "Content-Disposition": 'attachment; filename="character-classes.odt"'
        },
    )


@router.get("/character_classes")
def export_character_class_profiles_alias(sort: str = "Name") -> Response:
    return export_character_class_profiles(sort)
