export default function HomePage({
  monsters,
  spells,
  characterClasses,
  ruleSections,
  loading,
  onOpen,
  onCreate,
}) {
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow hero-eyebrow"><span className="sparkle">✳</span> YOUR CAMPAIGN COMPENDIUM</div>
          <h1>A place for<br />the <em>extraordinary.</em></h1>
          <p>Every creature has a story. Every class has a calling. Keep monsters, spells, character classes, and rule sections together, ready for whatever comes next.</p>
          <div className="hero-actions">
            <button className="button button-light" onClick={() => onOpen("monsters")}>Explore your registries <span>→</span></button>
            <button className="text-button hero-add" onClick={() => onCreate("monsters")}>＋ Add a creature</button>
          </div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="orbit orbit-one" /><div className="orbit orbit-two" />
          <div className="moon">✳</div>
          <div className="sigil">G</div>
          <span className="art-star star-one">✦</span><span className="art-star star-two">·</span><span className="art-star star-three">✧</span>
          <span className="art-label">VOL. I <i>—</i> THE FIELD NOTES</span>
        </div>
      </section>

      <section className="stats-row" aria-label="Collection summary">
        <article className="stat-card">
          <div className="stat-icon monster-icon">♞</div>
          <div><span className="stat-label">CREATURES</span><strong>{loading ? "—" : monsters.length}</strong><span className="stat-sub">in your bestiary</span></div>
          <button className="stat-arrow" onClick={() => onOpen("monsters")} aria-label="Open monsters">↗</button>
        </article>
        <article className="stat-card">
          <div className="stat-icon spell-icon">✳</div>
          <div><span className="stat-label">INCANTATIONS</span><strong>{loading ? "—" : spells.length}</strong><span className="stat-sub">in your spellbook</span></div>
          <button className="stat-arrow" onClick={() => onOpen("spells")} aria-label="Open spells">↗</button>
        </article>
        <article className="stat-card">
          <div className="stat-icon class-icon">♜</div>
          <div><span className="stat-label">CHARACTER CLASSES</span><strong>{loading ? "—" : characterClasses.length}</strong><span className="stat-sub">in your handbook</span></div>
          <button className="stat-arrow" onClick={() => onOpen("character-classes")} aria-label="Open character classes">↗</button>
        </article>
        <article className="stat-card">
          <div className="stat-icon rule-icon">§</div>
          <div><span className="stat-label">RULE SECTIONS</span><strong>{loading ? "—" : ruleSections.length}</strong><span className="stat-sub">for quick reference</span></div>
          <button className="stat-arrow" onClick={() => onOpen("rule-sections")} aria-label="Open rule sections">↗</button>
        </article>
      </section>

      <section className="start-section">
        <div className="section-title">
          <div><div className="eyebrow">MAKE YOUR MARK</div><h2>Where to begin</h2></div>
          <span className="section-aside">A good story starts with a detail.</span>
        </div>
        <div className="start-grid">
          <button className="start-card" onClick={() => onCreate("monsters")}>
            <span className="card-number">01 / BESTIARY</span><span className="card-symbol">♞</span>
            <strong>Document a creature</strong><span>Add the curious, the dangerous, and the not-yet-named to your bestiary.</span>
            <span className="card-link">Create monster <b>→</b></span>
          </button>
          <button className="start-card" onClick={() => onCreate("spells")}>
            <span className="card-number">02 / SPELLBOOK</span><span className="card-symbol">✳</span>
            <strong>Record an incantation</strong><span>Save a spell's range, duration, and all the ways it changes a day.</span>
            <span className="card-link">Create spell <b>→</b></span>
          </button>
          <button className="start-card" onClick={() => onCreate("character-classes")}>
            <span className="card-number">03 / CHARACTER CLASSES</span><span className="card-symbol">♜</span>
            <strong>Shape a calling</strong><span>Document requirements, abilities, progression, and the path each class follows.</span>
            <span className="card-link">Create character class <b>→</b></span>
          </button>
          <button className="start-card" onClick={() => onCreate("rule-sections")}>
            <span className="card-number">04 / RULES</span><span className="card-symbol">§</span>
            <strong>Add a rule section</strong><span>Keep campaign rulings and reference material clear, searchable, and close at hand.</span>
            <span className="card-link">Create rule section <b>→</b></span>
          </button>
        </div>
      </section>
    </>
  );
}
