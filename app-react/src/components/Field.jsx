import RichTextField from "../RichTextField";

export default function Field({
  label,
  value,
  onChange,
  type = "text",
  required = false,
  min,
  max,
  placeholder,
  hint,
  rows,
  richText = false,
}) {
  const id = `field-${label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;
  if (richText) {
    return (
      <div className={`form-field ${rows ? "field-full" : ""}`}>
        <label htmlFor={id}>
          <span>{label}{required && <i> *</i>}</span>
        </label>
        <RichTextField
          id={id}
          value={value ?? ""}
          onChange={onChange}
          required={required}
          placeholder={placeholder}
        />
        {hint && <small>{hint}</small>}
      </div>
    );
  }
  return (
    <label className={`form-field ${rows ? "field-full" : ""}`} htmlFor={id}>
      <span>{label}{required && <i> *</i>}</span>
      {rows ? (
        <textarea
          id={id}
          rows={rows}
          value={value ?? ""}
          placeholder={placeholder}
          onChange={(event) => onChange(event.target.value)}
          required={required}
        />
      ) : (
        <input
          id={id}
          type={type}
          min={min}
          max={max}
          value={value ?? ""}
          placeholder={placeholder}
          onChange={(event) => onChange(
            type === "number" ? Number(event.target.value) : event.target.value,
          )}
          required={required}
        />
      )}
      {hint && <small>{hint}</small>}
    </label>
  );
}
