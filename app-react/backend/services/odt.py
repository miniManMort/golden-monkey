"""OpenDocument Text serialization for monster and spell profiles."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile
from io import BytesIO

from ..schemas.monster import MonsterRead
from ..schemas.spell import SpellRead
from ..schemas.character_class import CharacterClassRead
from ..schemas.rule_section import RuleSectionRead

ODT_MIMETYPE = "application/vnd.oasis.opendocument.text"
OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
STYLE_NS = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
TABLE_NS = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
FO_NS = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"

_RICH_TEXT_TAGS = re.compile(
    r"<\/?(?:p|div|h[1-6]|br|strong|b|em|i|ul|ol|li|table|thead|tbody|tr|th|td)\b",
    re.IGNORECASE,
)
_DROP_CONTENT_TAGS = {"script", "style", "iframe", "object"}

ET.register_namespace("office", OFFICE_NS)
ET.register_namespace("text", TEXT_NS)
ET.register_namespace("style", STYLE_NS)
ET.register_namespace("table", TABLE_NS)
ET.register_namespace("fo", FO_NS)


def _tag(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def _set_multiline_text(element: ET.Element, value: str) -> None:
    lines = value.split("\n")
    element.text = lines[0]
    for line in lines[1:]:
        ET.SubElement(element, _tag(TEXT_NS, "line-break")).tail = line


@dataclass
class _HtmlNode:
    tag: str
    children: list[str | "_HtmlNode"] = field(default_factory=list)


class _RichTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.root = _HtmlNode("root")
        self.stack = [self.root]
        self.ignored_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        tag = tag.lower()
        if self.ignored_tags:
            if tag in _DROP_CONTENT_TAGS:
                self.ignored_tags.append(tag)
            return
        if tag in _DROP_CONTENT_TAGS:
            self.ignored_tags.append(tag)
            return
        node = _HtmlNode(tag)
        self.stack[-1].children.append(node)
        if tag != "br":
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() != "br" and not self.ignored_tags:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.ignored_tags:
            if tag == self.ignored_tags[-1]:
                self.ignored_tags.pop()
            return
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if not self.ignored_tags:
            self.stack[-1].children.append(data)


def _append_text(element: ET.Element, value: str) -> None:
    if len(element):
        element[-1].tail = (element[-1].tail or "") + value
    else:
        element.text = (element.text or "") + value


def _append_inline(
    element: ET.Element,
    children: list[str | _HtmlNode],
    bold: bool = False,
    italic: bool = False,
) -> None:
    for child in children:
        if isinstance(child, str):
            if not child:
                continue
            if bold or italic:
                style_name = "BoldItalic" if bold and italic else "Bold" if bold else "Italic"
                span = ET.SubElement(
                    element, _tag(TEXT_NS, "span"), {_tag(TEXT_NS, "style-name"): style_name}
                )
                span.text = child
            else:
                _append_text(element, child)
            continue

        if child.tag == "br":
            ET.SubElement(element, _tag(TEXT_NS, "line-break"))
            continue
        _append_inline(
            element,
            child.children,
            bold or child.tag in {"b", "strong"},
            italic or child.tag in {"i", "em"},
        )


def _descendants(node: _HtmlNode, tag: str) -> list[_HtmlNode]:
    found = []
    for child in node.children:
        if isinstance(child, _HtmlNode):
            if child.tag == tag:
                found.append(child)
            found.extend(_descendants(child, tag))
    return found


def _append_list(element: ET.Element, node: _HtmlNode) -> None:
    listing = ET.SubElement(element, _tag(TEXT_NS, "list"))
    for item in (child for child in node.children if isinstance(child, _HtmlNode) and child.tag == "li"):
        list_item = ET.SubElement(listing, _tag(TEXT_NS, "list-item"))
        paragraph = ET.SubElement(list_item, _tag(TEXT_NS, "p"))
        _append_inline(paragraph, item.children)


def _append_table(element: ET.Element, node: _HtmlNode, table_index: int) -> None:
    rows = _descendants(node, "tr")
    if not rows:
        return
    table = ET.SubElement(
        element,
        _tag(TABLE_NS, "table"),
        {_tag(TABLE_NS, "name"): f"RichTextTable_{table_index}"},
    )
    cells_by_row = [
        [child for child in row.children if isinstance(child, _HtmlNode) and child.tag in {"td", "th"}]
        for row in rows
    ]
    for _ in range(max(map(len, cells_by_row), default=0)):
        ET.SubElement(table, _tag(TABLE_NS, "table-column"))
    for cells in cells_by_row:
        row_element = ET.SubElement(table, _tag(TABLE_NS, "table-row"))
        for cell in cells:
            cell_element = ET.SubElement(
                row_element,
                _tag(TABLE_NS, "table-cell"),
                {_tag(OFFICE_NS, "value-type"): "string"},
            )
            paragraph = ET.SubElement(cell_element, _tag(TEXT_NS, "p"))
            _append_inline(paragraph, cell.children)


def _append_rich_content(
    element: ET.Element, value: str, table_counter: list[int]
) -> None:
    if not _RICH_TEXT_TAGS.search(value):
        paragraph = ET.SubElement(element, _tag(TEXT_NS, "p"))
        _set_multiline_text(paragraph, value)
        return

    parser = _RichTextParser()
    parser.feed(value)
    paragraph: ET.Element | None = None
    for child in parser.root.children:
        if isinstance(child, str):
            if not child.strip() and paragraph is None:
                continue
            if paragraph is None:
                paragraph = ET.SubElement(element, _tag(TEXT_NS, "p"))
            _append_text(paragraph, child)
        elif child.tag in {"p", "div"}:
            paragraph = ET.SubElement(element, _tag(TEXT_NS, "p"))
            _append_inline(paragraph, child.children)
        elif child.tag in {"ul", "ol"}:
            paragraph = None
            _append_list(element, child)
        elif child.tag == "table":
            paragraph = None
            table_counter[0] += 1
            _append_table(element, child, table_counter[0])
        elif child.tag == "br":
            if paragraph is None:
                paragraph = ET.SubElement(element, _tag(TEXT_NS, "p"))
            ET.SubElement(paragraph, _tag(TEXT_NS, "line-break"))
        else:
            if paragraph is None:
                paragraph = ET.SubElement(element, _tag(TEXT_NS, "p"))
            _append_inline(paragraph, [child])
    if paragraph is None and not len(element):
        ET.SubElement(element, _tag(TEXT_NS, "p"))


def _add_table_cell(row: ET.Element, value: str) -> None:
    cell = ET.SubElement(
        row,
        _tag(TABLE_NS, "table-cell"),
        {_tag(OFFICE_NS, "value-type"): "string"},
    )
    paragraph = ET.SubElement(cell, _tag(TEXT_NS, "p"))
    _set_multiline_text(paragraph, value)


def _make_monster_content(monsters: list[MonsterRead]) -> bytes:
    root = ET.Element(
        _tag(OFFICE_NS, "document-content"),
        {_tag(OFFICE_NS, "version"): "1.2"},
    )
    ET.SubElement(root, _tag(OFFICE_NS, "automatic-styles"))
    text = ET.SubElement(
        ET.SubElement(root, _tag(OFFICE_NS, "body")), _tag(OFFICE_NS, "text")
    )
    heading = ET.SubElement(
        text, _tag(TEXT_NS, "h"), {_tag(TEXT_NS, "outline-level"): "1"}
    )
    heading.text = "Monster Profiles"
    fields = (
        ("Summary", "summary"),
        ("Level", "level"),
        ("Hit Points", "hit_points"),
        ("Armour Class", "armour_class"),
        ("Save As", "save_as"),
        ("Morale", "morale"),
        ("Attacks", "attacks"),
        ("Damage", "damage"),
        ("Treasure", "treasure"),
        ("Alignment", "alignment"),
        ("Specials", "specials"),
    )
    table_counter = [0]
    for monster in monsters:
        monster_heading = ET.SubElement(
            text,
            _tag(TEXT_NS, "h"),
            {
                _tag(TEXT_NS, "outline-level"): "2",
                _tag(TEXT_NS, "style-name"): "Heading_20_2",
            },
        )
        _set_multiline_text(monster_heading, monster.name)
        for label, field in fields:
            value = getattr(monster, field)
            if field in {"summary", "specials"} and _RICH_TEXT_TAGS.search(value):
                paragraph = ET.SubElement(text, _tag(TEXT_NS, "p"))
                _set_multiline_text(paragraph, f"{label}:")
                _append_rich_content(text, value, table_counter)
            else:
                paragraph = ET.SubElement(text, _tag(TEXT_NS, "p"))
                _set_multiline_text(paragraph, f"{label}: {value}")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _make_spell_content(spells: list[SpellRead]) -> bytes:
    root = ET.Element(
        _tag(OFFICE_NS, "document-content"),
        {_tag(OFFICE_NS, "version"): "1.2"},
    )
    ET.SubElement(root, _tag(OFFICE_NS, "automatic-styles"))
    text = ET.SubElement(
        ET.SubElement(root, _tag(OFFICE_NS, "body")), _tag(OFFICE_NS, "text")
    )
    heading = ET.SubElement(
        text, _tag(TEXT_NS, "h"), {_tag(TEXT_NS, "outline-level"): "1"}
    )
    heading.text = "Spell Profiles"

    table_counter = [0]
    for index, spell in enumerate(spells):
        if index:
            ET.SubElement(text, _tag(TEXT_NS, "p"))
        spell_heading = ET.SubElement(
            text,
            _tag(TEXT_NS, "h"),
            {
                _tag(TEXT_NS, "outline-level"): "2",
                _tag(TEXT_NS, "style-name"): "Heading_20_2",
            },
        )
        _set_multiline_text(spell_heading, spell.name)
        table = ET.SubElement(
            text,
            _tag(TABLE_NS, "table"),
            {_tag(TABLE_NS, "name"): f"Spell_{index + 1}"},
        )
        for _ in range(4):
            ET.SubElement(table, _tag(TABLE_NS, "table-column"))
        headers = ET.SubElement(table, _tag(TABLE_NS, "table-row"))
        for value in ("Level", "Range", "Duration", "Save Allowed"):
            _add_table_cell(headers, value)
        values = ET.SubElement(table, _tag(TABLE_NS, "table-row"))
        for value in (
            str(spell.level),
            spell.range,
            spell.duration,
            spell.save_allowed,
        ):
            _add_table_cell(values, value)
        _append_rich_content(text, spell.effect, table_counter)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _make_character_class_content(
    character_classes: list[CharacterClassRead],
) -> bytes:
    root = ET.Element(
        _tag(OFFICE_NS, "document-content"),
        {_tag(OFFICE_NS, "version"): "1.2"},
    )
    ET.SubElement(root, _tag(OFFICE_NS, "automatic-styles"))
    text = ET.SubElement(
        ET.SubElement(root, _tag(OFFICE_NS, "body")), _tag(OFFICE_NS, "text")
    )
    heading = ET.SubElement(
        text, _tag(TEXT_NS, "h"), {_tag(TEXT_NS, "outline-level"): "1"}
    )
    heading.text = "Character Class Profiles"
    fields = (
        ("Outline", "outline"),
        ("Requirements", "requirements"),
        ("Hit Dice", "hit_dice"),
        ("Combat Skills", "combat_skills"),
        ("Other Skills", "other_skills"),
        ("Progression Table", "progression_table"),
    )
    table_counter = [0]
    for character_class in character_classes:
        class_heading = ET.SubElement(
            text,
            _tag(TEXT_NS, "h"),
            {
                _tag(TEXT_NS, "outline-level"): "2",
                _tag(TEXT_NS, "style-name"): "Heading_20_2",
            },
        )
        _set_multiline_text(class_heading, character_class.name)
        for label, field in fields:
            value = getattr(character_class, field)
            if field == "progression_table" and _RICH_TEXT_TAGS.search(value):
                paragraph = ET.SubElement(text, _tag(TEXT_NS, "p"))
                _set_multiline_text(paragraph, f"{label}:")
                _append_rich_content(text, value, table_counter)
            else:
                paragraph = ET.SubElement(text, _tag(TEXT_NS, "p"))
                _set_multiline_text(paragraph, f"{label}: {value}")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _make_rule_section_content(rule_sections: list[RuleSectionRead]) -> bytes:
    root = ET.Element(
        _tag(OFFICE_NS, "document-content"),
        {_tag(OFFICE_NS, "version"): "1.2"},
    )
    ET.SubElement(root, _tag(OFFICE_NS, "automatic-styles"))
    text = ET.SubElement(
        ET.SubElement(root, _tag(OFFICE_NS, "body")), _tag(OFFICE_NS, "text")
    )
    title = ET.SubElement(
        text, _tag(TEXT_NS, "h"), {_tag(TEXT_NS, "outline-level"): "1"}
    )
    title.text = "Rule Sections"
    table_counter = [0]
    for rule_section in rule_sections:
        heading = ET.SubElement(
            text,
            _tag(TEXT_NS, "h"),
            {
                _tag(TEXT_NS, "outline-level"): "2",
                _tag(TEXT_NS, "style-name"): "Heading_20_2",
            },
        )
        _set_multiline_text(heading, rule_section.name)
        _append_rich_content(text, rule_section.section_text, table_counter)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _make_styles() -> bytes:
    root = ET.Element(
        _tag(OFFICE_NS, "document-styles"),
        {_tag(OFFICE_NS, "version"): "1.2"},
    )
    styles = ET.SubElement(root, _tag(OFFICE_NS, "styles"))
    heading_style = ET.SubElement(
        styles,
        _tag(STYLE_NS, "style"),
        {
            _tag(STYLE_NS, "name"): "Heading_20_2",
            _tag(STYLE_NS, "display-name"): "Heading 2",
            _tag(STYLE_NS, "family"): "paragraph",
        },
    )
    ET.SubElement(
        heading_style,
        _tag(STYLE_NS, "paragraph-properties"),
        {
            _tag(FO_NS, "margin-top"): "0.18in",
            _tag(FO_NS, "margin-bottom"): "0.08in",
            _tag(FO_NS, "keep-with-next"): "always",
        },
    )
    ET.SubElement(
        heading_style,
        _tag(STYLE_NS, "text-properties"),
        {_tag(FO_NS, "font-size"): "14pt", _tag(FO_NS, "font-weight"): "bold"},
    )
    for name, properties in (
        ("Bold", {_tag(FO_NS, "font-weight"): "bold"}),
        ("Italic", {_tag(FO_NS, "font-style"): "italic"}),
        (
            "BoldItalic",
            {
                _tag(FO_NS, "font-weight"): "bold",
                _tag(FO_NS, "font-style"): "italic",
            },
        ),
    ):
        style = ET.SubElement(
            styles,
            _tag(STYLE_NS, "style"),
            {
                _tag(STYLE_NS, "name"): name,
                _tag(STYLE_NS, "family"): "text",
            },
        )
        ET.SubElement(style, _tag(STYLE_NS, "text-properties"), properties)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _make_manifest() -> bytes:
    manifest = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" '
        'manifest:version="1.2">'
        f'<manifest:file-entry manifest:full-path="/" manifest:media-type="{ODT_MIMETYPE}"/>'
        '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>'
        '<manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>'
        "</manifest:manifest>"
    )
    return manifest.encode("utf-8")


def _make_odt(content: bytes) -> bytes:
    output = BytesIO()
    with ZipFile(output, "w") as archive:
        archive.writestr("mimetype", ODT_MIMETYPE, compress_type=ZIP_STORED)
        archive.writestr("content.xml", content, compress_type=ZIP_DEFLATED)
        archive.writestr("styles.xml", _make_styles(), compress_type=ZIP_DEFLATED)
        archive.writestr(
            "META-INF/manifest.xml", _make_manifest(), compress_type=ZIP_DEFLATED
        )
    return output.getvalue()


def export_monsters(monsters: list[MonsterRead]) -> bytes:
    return _make_odt(_make_monster_content(monsters))


def export_spells(spells: list[SpellRead]) -> bytes:
    return _make_odt(_make_spell_content(spells))


def export_character_classes(
    character_classes: list[CharacterClassRead],
) -> bytes:
    return _make_odt(_make_character_class_content(character_classes))


def export_rule_sections(rule_sections: list[RuleSectionRead]) -> bytes:
    return _make_odt(_make_rule_section_content(rule_sections))
