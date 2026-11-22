import { useMemo, useState } from "react";
import {
  CHARACTER_CLASS_COLUMNS,
  MONSTER_COLUMNS,
  RULE_SECTION_COLUMNS,
  SPELL_COLUMNS,
} from "../config/records";

export default function RecordTable({ kind, records, onView, onEdit }) {
  const isMonster = kind === "monsters";
  const isCharacterClass = kind === "character-classes";
  const isRuleSection = kind === "rule-sections";
  const columns = isMonster
    ? MONSTER_COLUMNS
    : isCharacterClass
      ? CHARACTER_CLASS_COLUMNS
      : isRuleSection
        ? RULE_SECTION_COLUMNS
        : SPELL_COLUMNS;
  const [field, setField] = useState("name");
  const [query, setQuery] = useState("");
  const [applied, setApplied] = useState({ field: "name", query: "" });
  const [searchError, setSearchError] = useState("");
  const filtered = useMemo(() => {
    if (!applied.query) return records;
    const regex = new RegExp(applied.query, "i");
    return records.filter((record) => regex.test(String(record[applied.field])));
  }, [records, applied]);

  function search(event) {
    event.preventDefault();
    try {
      if (query) new RegExp(query, "i");
      setApplied({ field, query });
      setSearchError("");
    } catch (error) {
      setSearchError(`Invalid regular expression: ${error.message}`);
    }
  }

  return (
    <>
      <div className="table-toolbar">
        <form className="search-form" onSubmit={search}>
          <label className="search-select">
            <span className="sr-only">Search field</span>
            <select value={field} onChange={(event) => setField(event.target.value)}>
              {(isMonster
                ? [["name", "Name"], ["level", "Level"], ["alignment", "Alignment"]]
                : isCharacterClass
                  ? [["name", "Name"], ["hit_dice", "Hit Dice"], ["requirements", "Requirements"]]
                  : isRuleSection
                    ? [["name", "Name"]]
                    : [["name", "Name"], ["level", "Level"]]
              ).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </label>
          <label className="search-input">
            <span className="search-glass">⌕</span>
            <span className="sr-only">Regular expression search</span>
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search with a regular expression…" />
            {query && <button type="button" className="clear-search" onClick={() => setQuery("")} aria-label="Clear search">×</button>}
          </label>
          <button className="button button-dark" type="submit">Search</button>
        </form>
        <span className="result-count">{filtered.length} {filtered.length === 1 ? "record" : "records"}</span>
      </div>
      {searchError && <p className="inline-error" role="alert">{searchError}</p>}
      <div className="table-wrap">
        <table>
          <thead><tr>{columns.map(([, label]) => <th key={label}>{label}</th>)}<th className="action-heading">ACTIONS</th></tr></thead>
          <tbody>
            {filtered.map((record) => (
              <tr key={record.id}>
                {columns.map(([key]) => (
                  <td key={key}>{key === "name"
                    ? <strong className="record-name">{record[key]}</strong>
                    : record[key]}</td>
                ))}
                <td className="table-actions">
                  <button className="table-action" onClick={() => onView(record)}>View</button>
                  <button className="table-action edit-action" onClick={() => onEdit(record)}>Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div className="empty-state">
            <span className="empty-symbol">{isMonster ? "♞" : "✳"}</span>
            <strong>{records.length === 0 ? `Your ${isMonster ? "bestiary" : isCharacterClass ? "character classes" : "spellbook"} is waiting.` : "No matching records."}</strong>
            <span>{records.length === 0 ? "Add the first entry to start building your collection." : "Try another expression or clear your search."}</span>
          </div>
        )}
      </div>
      <div className="table-footnote">
        <span><span className="status-dot" /> Saved automatically to your local library</span>
        <span>Use View for the full profile · Edit to make a change</span>
      </div>
    </>
  );
}
