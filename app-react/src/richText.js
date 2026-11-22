import React from "react";

const RICH_TAGS = "p|div|h1|h2|h3|h4|h5|h6|br|strong|b|em|i|ul|ol|li|table|thead|tbody|tr|th|td";
const RICH_TAG_PATTERN = new RegExp(`<\\/?(?:${RICH_TAGS})\\b`, "i");
const ALLOWED_TAGS = new Set(RICH_TAGS.split("|"));
const DROP_CONTENT_TAGS = new Set(["script", "style", "iframe", "object"]);

function copyAllowedChildren(source, target) {
  for (const child of source.childNodes) {
    if (child.nodeType === Node.TEXT_NODE) {
      target.append(document.createTextNode(child.nodeValue || ""));
      continue;
    }
    if (child.nodeType !== Node.ELEMENT_NODE) continue;

    const tag = child.tagName.toLowerCase();
    if (DROP_CONTENT_TAGS.has(tag)) continue;
    if (!ALLOWED_TAGS.has(tag)) {
      copyAllowedChildren(child, target);
      continue;
    }
    const element = document.createElement(tag);
    copyAllowedChildren(child, element);
    target.append(element);
  }
}

export function sanitizeRichHtml(value) {
  const parsed = new DOMParser().parseFromString(value || "", "text/html");
  const safe = document.createElement("div");
  copyAllowedChildren(parsed.body, safe);
  return safe.innerHTML;
}

export function toEditorHtml(value) {
  const text = value || "";
  if (!text) return "<p><br></p>";
  if (RICH_TAG_PATTERN.test(text)) return sanitizeRichHtml(text);
  return text
    .split(/\r?\n/)
    .map((line) => `<p>${line.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;") || "<br>"}</p>`)
    .join("");
}

function renderChildren(parent, keyPrefix) {
  return Array.from(parent.childNodes).flatMap((node, index) => {
    const key = `${keyPrefix}-${index}`;
    if (node.nodeType === Node.TEXT_NODE) return [node.nodeValue || ""];
    if (node.nodeType !== Node.ELEMENT_NODE) return [];

    const tag = node.tagName.toLowerCase();
    const children = renderChildren(node, key);
    if (DROP_CONTENT_TAGS.has(tag)) return [];
    if (!ALLOWED_TAGS.has(tag)) return children;
    return [React.createElement(tag, { key }, children)];
  });
}

export function renderRichText(value) {
  const text = value || "";
  if (!RICH_TAG_PATTERN.test(text)) return text;
  const parsed = new DOMParser().parseFromString(sanitizeRichHtml(text), "text/html");
  return renderChildren(parsed.body, "rich");
}

export function countRichTextCharacters(value) {
  const text = value || "";
  if (!RICH_TAG_PATTERN.test(text)) return text.length;
  const parsed = new DOMParser().parseFromString(sanitizeRichHtml(text), "text/html");
  return parsed.body.textContent.length;
}
