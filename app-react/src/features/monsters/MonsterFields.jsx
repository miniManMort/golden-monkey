import Field from "../../components/Field";
import { countRichTextCharacters } from "../../richText";

export default function MonsterFields({ values, update }) {
  return (
    <div className="form-grid">
      <Field label="Name" value={values.name} onChange={(value) => update("name", value)} required placeholder="e.g. Mossback troll" />
      <Field label="Level" type="number" min="1" max="20" value={values.level} onChange={(value) => update("level", value)} required />
      <Field label="Summary" value={values.summary} onChange={(value) => update("summary", value)} required rows={3} richText hint={`${countRichTextCharacters(values.summary)} / 60 characters minimum`} placeholder="Describe the creature, its nature, and where it is found…" />
      <div className="field-pair">
        <Field label="HP" value={values.hit_points} onChange={(value) => update("hit_points", value)} required placeholder="2d8+1" />
        <Field label="AC" type="number" min="5" max="25" value={values.armour_class} onChange={(value) => update("armour_class", value)} required />
      </div>
      <div className="field-pair">
        <Field label="Save" value={values.save_as} onChange={(value) => update("save_as", value)} required placeholder="F:1" />
        <Field label="Morale" type="number" min="2" max="12" value={values.morale} onChange={(value) => update("morale", value)} required />
      </div>
      <Field label="Attacks" value={values.attacks} onChange={(value) => update("attacks", value)} required placeholder="1 bite" />
      <Field label="Damage" value={values.damage} onChange={(value) => update("damage", value)} required placeholder="1d6" />
      <Field label="Treasure" value={values.treasure} onChange={(value) => update("treasure", value)} placeholder="Nil" />
      <label className="form-field" htmlFor="field-alignment">
        <span>Alignment *</span>
        <select id="field-alignment" value={values.alignment} onChange={(event) => update("alignment", event.target.value)}>
          <option>Lawful</option>
          <option>Chaotic</option>
          <option>Neutral</option>
        </select>
      </label>
      <Field label="Specials" value={values.specials} onChange={(value) => update("specials", value)} rows={3} richText placeholder="None" />
    </div>
  );
}
