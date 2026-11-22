export const EMPTY_MONSTER = {
  name: "",
  summary: "",
  level: 1,
  hit_points: "",
  armour_class: 10,
  save_as: "",
  morale: 5,
  attacks: "",
  damage: "",
  treasure: "Nil",
  alignment: "Neutral",
  specials: "None",
};

export const EMPTY_SPELL = {
  name: "",
  level: 1,
  save_allowed: "",
  range: "",
  duration: "",
  effect: "None",
};

export const EMPTY_CHARACTER_CLASS = {
  name: "",
  outline: "",
  requirements: "",
  hit_dice: "d6",
  combat_skills: "",
  other_skills: "",
  progression_table: "",
};

export const MONSTER_COLUMNS = [
  ["name", "Name"],
  ["level", "Level"],
  ["armour_class", "AC"],
  ["save_as", "Save"],
  ["morale", "Morale"],
  ["alignment", "Alignment"],
];

export const SPELL_COLUMNS = [
  ["name", "Name"],
  ["level", "Level"],
  ["range", "Range"],
  ["duration", "Duration"],
  ["save_allowed", "Save Allowed"],
];

export const CHARACTER_CLASS_COLUMNS = [
  ["name", "Name"],
  ["hit_dice", "Hit Dice"],
  ["requirements", "Requirements"],
];
