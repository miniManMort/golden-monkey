import Field from "../../components/Field";

export default function SpellFields({ values, update }) {
  return (
    <div className="form-grid">
      <Field label="Name" value={values.name} onChange={(value) => update("name", value)} required placeholder="e.g. Lantern of the moon" />
      <Field label="Level" type="number" min="1" max="6" value={values.level} onChange={(value) => update("level", value)} required />
      <Field label="Save allowed" value={values.save_allowed} onChange={(value) => update("save_allowed", value)} required placeholder="None, half, negates…" />
      <Field label="Range" value={values.range} onChange={(value) => update("range", value)} required placeholder="Touch" />
      <Field label="Duration" value={values.duration} onChange={(value) => update("duration", value)} required placeholder="1 hour" />
      <Field label="Effect" value={values.effect} onChange={(value) => update("effect", value)} required rows={5} richText placeholder="Describe what the spell does…" />
    </div>
  );
}
