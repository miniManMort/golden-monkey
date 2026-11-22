import Field from "../../components/Field";

export default function RuleSectionFields({ values, update }) {
  return (
    <div className="form-grid">
      <Field
        label="Name"
        value={values.name}
        onChange={(value) => update("name", value)}
        required
        placeholder="e.g. Combat"
      />
      <Field
        label="Section text"
        value={values.section_text}
        onChange={(value) => update("section_text", value)}
        required
        rows={8}
        richText
        placeholder="Describe the rules for this section."
      />
    </div>
  );
}
