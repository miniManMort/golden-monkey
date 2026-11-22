import { useEffect, useState } from "react";
import { libraryApi } from "./api/client";
import DetailsDialog from "./components/DetailsDialog";
import ExportDialog from "./components/ExportDialog";
import HelpDialog from "./components/HelpDialog";
import RecordDialog from "./components/RecordDialog";
import RecordTable from "./components/RecordTable";
import HomePage from "./pages/HomePage";

export default function App() {
  const [page, setPage] = useState("home");
  const [monsters, setMonsters] = useState([]);
  const [spells, setSpells] = useState([]);
  const [characterClasses, setCharacterClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [dialog, setDialog] = useState(null);
  const [helpOpen, setHelpOpen] = useState(false);

  async function refreshRecords() {
    setLoadError("");
    try {
      const [monsterRows, spellRows, characterClassRows] = await Promise.all([
        libraryApi.getMonsters(),
        libraryApi.getSpells(),
        libraryApi.getCharacterClasses(),
      ]);
      setMonsters(monsterRows);
      setSpells(spellRows);
      setCharacterClasses(characterClassRows);
    } catch (error) {
      setLoadError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refreshRecords();
  }, []);

  const isMonster = page === "monsters";
  const isCharacterClass = page === "character-classes";
  const activeItems = isMonster
    ? monsters
    : isCharacterClass
      ? characterClasses
      : spells;
  const title = isMonster
    ? "Monster registry"
    : isCharacterClass
      ? "Character classes"
      : "Spellbook";

  function openCreate(kind) {
    setDialog({ mode: "edit", kind, record: null });
  }

  async function handleDelete(kind, record) {
    const recordType = kind === "monsters"
      ? "monster"
      : kind === "character-classes"
        ? "character class"
        : "spell";
    if (!window.confirm(`Delete this ${recordType}, "${record.name}"? This cannot be undone. Continue?`)) return;
    try {
      await (kind === "monsters"
        ? libraryApi.deleteMonster(record)
        : kind === "character-classes"
          ? libraryApi.deleteCharacterClass(record)
          : libraryApi.deleteSpell(record));
      setDialog(null);
      await refreshRecords();
    } catch (error) {
      setLoadError(error.message);
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={() => setPage("home")} aria-label="Golden Monkey home">
          <span className="brand-mark">GM</span>
          <span><strong>Golden Monkey</strong><small>FIELD GUIDE</small></span>
        </button>
        <div className="nav-caption">WORKSPACE</div>
        <nav className="main-nav" aria-label="Main navigation">
          <button className={page === "home" ? "nav-item active" : "nav-item"} onClick={() => setPage("home")}>
            <span className="nav-icon">⌂</span> Overview
          </button>
          <button className={page === "monsters" ? "nav-item active" : "nav-item"} onClick={() => setPage("monsters")}>
            <span className="nav-icon">♞</span> Monsters <span className="nav-count">{monsters.length}</span>
          </button>
          <button className={page === "spells" ? "nav-item active" : "nav-item"} onClick={() => setPage("spells")}>
            <span className="nav-icon">✳</span> Spells <span className="nav-count">{spells.length}</span>
          </button>
          <button className={page === "character-classes" ? "nav-item active" : "nav-item"} onClick={() => setPage("character-classes")}>
            <span className="nav-icon">♜</span> Classes <span className="nav-count">{characterClasses.length}</span>
          </button>
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-note">
            <span className="status-dot" />
            <span>Local library<br /><strong>SQLite connected</strong></span>
          </div>
          <button className="help-link" onClick={() => setHelpOpen(true)}>
            <span className="nav-icon">?</span> Help &amp; about
          </button>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            <span>LIBRARY</span><span className="crumb-divider">/</span>
            <strong>{page === "home" ? "OVERVIEW" : page.toUpperCase()}</strong>
          </div>
          <div className="topbar-actions">
            <span className="connection-label"><span className="status-dot" /> Connected</span>
            <button className="avatar" onClick={() => setHelpOpen(true)} aria-label="About Golden Monkey">G</button>
          </div>
        </header>

        <div className="page-content">
          {loadError && (
            <div className="alert error-alert" role="alert">
              <span>{loadError}</span>
              <button onClick={() => setLoadError("")} aria-label="Dismiss error">×</button>
            </div>
          )}
          {page === "home" ? (
            <HomePage
              monsters={monsters}
              spells={spells}
              characterClasses={characterClasses}
              loading={loading}
              onOpen={setPage}
              onCreate={openCreate}
            />
          ) : (
            <section>
              <div className="page-heading">
                <div>
                  <div className="eyebrow">YOUR COLLECTION</div>
                  <h1>{title}</h1>
                  <p>{isMonster
                    ? "Catalog creatures, their habits, and their hard-won statistics."
                    : isCharacterClass
                      ? "Maintain character classes, requirements, abilities, and progression."
                      : "Keep every incantation, its reach, and its effects close at hand."}</p>
                </div>
                <div className="heading-actions">
                  <button className="button button-outline" onClick={() => setDialog({ mode: "export", kind: page })}>
                    <span>↓</span> Export
                  </button>
                  <button className="button button-primary" onClick={() => openCreate(page)}>
                    <span>＋</span> Add {isMonster ? "monster" : isCharacterClass ? "class" : "spell"}
                  </button>
                </div>
              </div>
              {loading ? (
                <div className="empty-panel">Loading your library…</div>
              ) : (
                <RecordTable
                  kind={page}
                  records={activeItems}
                  onView={(record) => setDialog({ mode: "view", kind: page, record })}
                  onEdit={(record) => setDialog({ mode: "edit", kind: page, record })}
                />
              )}
            </section>
          )}
        </div>
        <footer className="page-footer">
          <span>GOLDEN MONKEY</span>
          <span>YOUR ADVENTURE, WELL DOCUMENTED.</span>
        </footer>
      </main>

      {dialog?.mode === "edit" && (
        <RecordDialog
          kind={dialog.kind}
          record={dialog.record}
          onClose={() => setDialog(null)}
          onSaved={async () => {
            setDialog(null);
            await refreshRecords();
          }}
          onDelete={() => handleDelete(dialog.kind, dialog.record)}
        />
      )}
      {dialog?.mode === "view" && (
        <DetailsDialog
          kind={dialog.kind}
          record={dialog.record}
          onClose={() => setDialog(null)}
          onEdit={() => setDialog({ ...dialog, mode: "edit" })}
        />
      )}
      {dialog?.mode === "export" && (
        <ExportDialog kind={dialog.kind} onClose={() => setDialog(null)} />
      )}
      {helpOpen && <HelpDialog onClose={() => setHelpOpen(false)} />}
    </div>
  );
}
