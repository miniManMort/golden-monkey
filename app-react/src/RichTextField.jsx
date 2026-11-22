import { Editor } from "@tinymce/tinymce-react";
import { sanitizeRichHtml, toEditorHtml } from "./richText";

export default function RichTextField({
  id,
  value,
  onChange,
  required = false,
  placeholder,
}) {
  return (
    <Editor
      id={id}
      licenseKey="gpl"
      tinymceScriptSrc="/tinymce/tinymce.min.js"
      value={toEditorHtml(value)}
      onEditorChange={(html) => onChange(sanitizeRichHtml(html))}
      init={{
        base_url: "/tinymce",
        suffix: ".min",
        menubar: false,
        branding: false,
        statusbar: false,
        resize: false,
        height: 230,
        min_height: 230,
        placeholder,
        plugins: "lists table",
        toolbar: "formatselect bold italic bullist table",
        block_formats: "Paragraph=p;Heading 1=h1;Heading 2=h2;Heading 3=h3",
        valid_elements: "p,h1,h2,h3,br,strong/b,em/i,ul,ol,li,table,thead,tbody,tr,th,td",
        convert_urls: false,
        skin: "oxide",
        content_css: "/tinymce/skins/content/default/content.css",
        content_style:
          "body { font-family: 'Avenir Next', Avenir, 'Segoe UI', Arial, sans-serif; font-size: 11px; line-height: 1.55; }",
        setup(editor) {
          if (required) {
            editor.on("PostRender", () => {
              editor.getContainer().setAttribute("aria-required", "true");
            });
          }
        },
      }}
    />
  );
}
