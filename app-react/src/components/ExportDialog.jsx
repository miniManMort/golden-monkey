import { useState } from "react";
import { libraryApi } from "../api/client";
import Modal from "./Modal";

export default function ExportDialog({ kind, onClose }) {
  const [sort, setSort] = useState("Name");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const label = kind === "monsters"
    ? "monster"
    : kind === "character-classes"
      ? "character class"
      : kind === "rule-sections"
        ? "rule section"
        : "spell";

  async function exportRecords(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const blob = await libraryApi.exportRecords(kind, sort);
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${kind}.odt`;
      document.body.append(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
      onClose();
    } catch (exportError) {
      setError(exportError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal onClose={onClose} labelledBy="export-title">
      <div className="modal-heading">
        <div><div className="eyebrow">TAKE IT WITH YOU</div><h2 id="export-title">Export {kind}</h2></div>
        <button className="icon-close" onClick={onClose} aria-label="Close dialog">×</button>
      </div>
      <p className="modal-intro">Create an OpenDocument Text file containing every {label} profile in your library.</p>
      <form onSubmit={exportRecords}>
        <label className="form-field" htmlFor="sort-order">
          <span>Sort profiles by</span>
          <select id="sort-order" value={sort} onChange={(event) => setSort(event.target.value)}>
            <option>Name</option>
            {kind === "character-classes"
              ? <option>Hit Dice / Name</option>
              : kind !== "rule-sections"
                ? <option>Level / Name</option>
                : null}
          </select>
        </label>
        {error && <div className="alert error-alert" role="alert">{error}</div>}
        <div className="export-format">
          <span className="file-icon">ODT</span>
          <span><strong>OpenDocument Text</strong><small>Compatible with LibreOffice and other document editors</small></span>
        </div>
        <div className="modal-actions">
          <span className="form-spacer" />
          <button type="button" className="button button-outline" onClick={onClose}>Cancel</button>
          <button className="button button-primary" disabled={busy}>{busy ? "Preparing…" : "Download .odt"}</button>
        </div>
      </form>
    </Modal>
  );
}
