import Modal from "./Modal";

export default function HelpDialog({ onClose }) {
  return (
    <Modal onClose={onClose} labelledBy="help-title">
      <div className="modal-heading">
        <div><div className="eyebrow">A NOTE FROM THE ARCHIVIST</div><h2 id="help-title">About Golden Monkey</h2></div>
        <button className="icon-close" onClick={onClose} aria-label="Close dialog">×</button>
      </div>
      <p className="modal-intro">Golden Monkey helps you create, update, and review the monsters and spells in your tabletop role-playing world. Your records are stored in the local SQLite library shared with the desktop app.</p>
      <div className="help-items">
        <div><strong>01</strong><span><b>Build your collection</b><small>Add detailed monster profiles and spell references.</small></span></div>
        <div><strong>02</strong><span><b>Find what you need</b><small>Search names, levels, or alignments with regular expressions.</small></span></div>
        <div><strong>03</strong><span><b>Take it along</b><small>Export profiles as OpenDocument Text files.</small></span></div>
      </div>
      <div className="modal-actions"><span className="form-spacer" /><button className="button button-primary" onClick={onClose}>Got it</button></div>
    </Modal>
  );
}
