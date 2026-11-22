import { renderRichText } from "../richText";
import Modal from "./Modal";

export default function DetailsDialog({ kind, record, onClose, onEdit }) {
  const fields = kind === "monsters"
    ? [
        ["Summary", "summary"], ["Level", "level"], ["HP", "hit_points"],
        ["AC", "armour_class"], ["Save", "save_as"], ["Morale", "morale"],
        ["Attacks", "attacks"], ["Damage", "damage"], ["Treasure", "treasure"],
        ["Alignment", "alignment"], ["Specials", "specials"],
      ]
    : kind === "character-classes"
      ? [
          ["Outline", "outline"], ["Requirements", "requirements"],
          ["Hit Dice", "hit_dice"], ["Combat Skills", "combat_skills"],
          ["Other Skills", "other_skills"], ["Progression Table", "progression_table"],
        ]
      : [
        ["Level", "level"], ["Save allowed", "save_allowed"],
        ["Range", "range"], ["Duration", "duration"], ["Effect", "effect"],
      ];
  return (
    <Modal onClose={onClose} labelledBy="details-title">
      <div className="modal-heading">
        <div>
          <div className="eyebrow">{kind === "monsters" ? "CREATURE PROFILE" : kind === "character-classes" ? "CHARACTER CLASS PROFILE" : "SPELL PROFILE"}</div>
          <h2 id="details-title">{record.name}</h2>
        </div>
        <button className="icon-close" onClick={onClose} aria-label="Close dialog">×</button>
      </div>
      <dl className="detail-list">
        <div className="detail-row"><dt>Name</dt><dd>{record.name}</dd></div>
        {fields.map(([label, key]) => (
          <div className="detail-row" key={key}>
            <dt>{label}</dt>
            <dd className={["summary", "effect", "specials", "progression_table"].includes(key) ? "detail-long" : ""}>
              {["summary", "effect", "specials", "progression_table"].includes(key)
                ? renderRichText(record[key])
                : record[key]}
            </dd>
          </div>
        ))}
      </dl>
      <div className="modal-actions">
        <span className="form-spacer" />
        <button className="button button-outline" onClick={onClose}>Close</button>
        <button className="button button-primary" onClick={onEdit}>Edit entry</button>
      </div>
    </Modal>
  );
}
