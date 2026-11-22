import Field from "../../components/Field";

export default function CharacterClassFields({ values, update }) {
  return (
    <div className="form-grid">
      <Field
        label="Name"
        value={values.name}
        onChange={(value) => update("name", value)}
        required
        placeholder="e.g. Ranger"
      />
      <label className="form-field" htmlFor="field-hit-dice">
        <span>Hit Dice <i>*</i></span>
        <select
          id="field-hit-dice"
          value={values.hit_dice}
          onChange={(event) => update("hit_dice", event.target.value)}
        >
          <option>d4</option>
          <option>d6</option>
          <option>d8</option>
          <option>d10</option>
        </select>
      </label>
      <Field
        label="Outline"
        value={values.outline}
        onChange={(value) => update("outline", value)}
        required
        rows={3}
        placeholder="Summarize the class and its role."
      />
      <Field
        label="Requirements"
        value={values.requirements}
        onChange={(value) => update("requirements", value)}
        required
        rows={3}
        placeholder="Ability scores or other prerequisites."
      />
      <Field
        label="Combat skills"
        value={values.combat_skills}
        onChange={(value) => update("combat_skills", value)}
        required
        rows={3}
        placeholder="Weapons, armor, and combat abilities."
      />
      <Field
        label="Other skills"
        value={values.other_skills}
        onChange={(value) => update("other_skills", value)}
        required
        rows={3}
        placeholder="Exploration, social, and class abilities."
      />
      <Field
        label="Progression table"
        value={values.progression_table}
        onChange={(value) => update("progression_table", value)}
        required
        rows={5}
        richText
        placeholder="Describe or table the class progression."
      />
    </div>
  );
}
