async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });
  const contentType = response.headers.get("content-type") || "";
  const result = contentType.includes("application/json")
    ? await response.json()
    : await response.blob();
  if (!response.ok) {
    throw new Error(result?.error || `Request failed (${response.status}).`);
  }
  return result;
}

export const libraryApi = {
  getMonsters: () => request("/api/monsters"),
  getSpells: () => request("/api/spells"),
  getCharacterClasses: () => request("/api/character-classes"),
  createMonster: (value) => request("/api/monsters", {
    method: "POST",
    body: JSON.stringify(value),
  }),
  updateMonster: (record, value) => request(`/api/monsters/${encodeURIComponent(record.id)}`, {
    method: "PUT",
    body: JSON.stringify(value),
  }),
  deleteMonster: (record) => request(`/api/monsters/${encodeURIComponent(record.id)}`, {
    method: "DELETE",
  }),
  createSpell: (value) => request("/api/spells", {
    method: "POST",
    body: JSON.stringify(value),
  }),
  updateSpell: (record, value) => request(`/api/spells/${encodeURIComponent(record.id)}`, {
    method: "PUT",
    body: JSON.stringify(value),
  }),
  deleteSpell: (record) => request(`/api/spells/${encodeURIComponent(record.id)}`, {
    method: "DELETE",
  }),
  createCharacterClass: (value) => request("/api/character-classes", {
    method: "POST",
    body: JSON.stringify(value),
  }),
  updateCharacterClass: (record, value) => request(
    `/api/character-classes/${encodeURIComponent(record.id)}`,
    { method: "PUT", body: JSON.stringify(value) },
  ),
  deleteCharacterClass: (record) => request(
    `/api/character-classes/${encodeURIComponent(record.id)}`,
    { method: "DELETE" },
  ),
  exportRecords: (kind, sort) => request(
    `/api/export/${kind}?sort=${encodeURIComponent(sort)}`,
  ),
};
