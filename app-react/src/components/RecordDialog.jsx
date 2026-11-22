import { useState } from "react";
import { libraryApi } from "../api/client";
import {
  EMPTY_CHARACTER_CLASS,
  EMPTY_MONSTER,
  EMPTY_SPELL,
} from "../config/records";
import CharacterClassFields from "../features/character-classes/CharacterClassFields";
import MonsterFields from "../features/monsters/MonsterFields";
import SpellFields from "../features/spells/SpellFields";
import { countRichTextCharacters } from "../richText";
import Modal from "./Modal";

export default function RecordDialog({ kind, record, onClose, onSaved, onDelete }) {
  const isMonster = kind === "monsters";
  const isCharacterClass = kind === "character-classes";
  const initial = record || (
    isMonster
      ? EMPTY_MONSTER
      : isCharacterClass
        ? EMPTY_CHARACTER_CLASS
        : EMPTY_SPELL
  );
  const [values, setValues] = useState({ ...initial });
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function update(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    setError("");
    if (isMonster && countRichTextCharacters(values.summary) === 0) {
      setError("Summary cannot be blank.");
      return;
    }
    if (
      !isMonster &&
      !isCharacterClass &&
      countRichTextCharacters(values.effect) === 0
    ) {
      setError("Effect cannot be blank.");
      return;
    }
    if (
      isCharacterClass &&
      countRichTextCharacters(values.progression_table) === 0
    ) {
      setError("Progression table cannot be blank.");
      return;
    }
    setSaving(true);
    try {
      if (record) {
        await (isMonster
          ? libraryApi.updateMonster(record, values)
          : isCharacterClass
            ? libraryApi.updateCharacterClass(record, values)
            : libraryApi.updateSpell(record, values));
      } else {
        await (isMonster
          ? libraryApi.createMonster(values)
          : isCharacterClass
            ? libraryApi.createCharacterClass(values)
            : libraryApi.createSpell(values));
      }
      await onSaved();
    } catch (saveError) {
      setError(saveError.message);
    } finally {
      setSaving(false);
    }
  }

  const title = `${record ? "Edit" : "Add"} ${
    isMonster ? "creature" : isCharacterClass ? "character class" : "incantation"
  }`;
  return (
    <Modal onClose={onClose} labelledBy="record-dialog-title" wide>
      <div className="modal-heading">
        <div>
          <div className="eyebrow">{isMonster ? "BESTIARY ENTRY" : isCharacterClass ? "CLASS ENTRY" : "SPELLBOOK ENTRY"}</div>
          <h2 id="record-dialog-title">{title}</h2>
        </div>
        <button className="icon-close" onClick={onClose} aria-label="Close dialog">×</button>
      </div>
      <form className="record-form" onSubmit={submit}>
        {isMonster
          ? <MonsterFields values={values} update={update} />
          : isCharacterClass
            ? <CharacterClassFields values={values} update={update} />
            : <SpellFields values={values} update={update} />}
        {error && <div className="alert error-alert" role="alert">{error}</div>}
        <div className="modal-actions">
          {record && (
            <button
              type="button"
              className="button button-danger"
              onClick={onDelete}
              aria-label={`Delete ${isMonster ? "monster" : isCharacterClass ? "character class" : "spell"} ${record.name}`}
            >
              Delete {isMonster ? "monster" : isCharacterClass ? "character class" : "spell"}
            </button>
          )}
          <span className="form-spacer" />
          <button type="button" className="button button-outline" onClick={onClose}>Cancel</button>
          <button className="button button-primary" disabled={saving}>{saving ? "Saving…" : record ? "Save changes" : "Create entry"}</button>
        </div>
      </form>
    </Modal>
  );
}
