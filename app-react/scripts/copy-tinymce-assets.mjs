import { cp, mkdir, rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const appDirectory = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const packageDirectory = resolve(appDirectory, "node_modules/tinymce");
const destination = resolve(appDirectory, "public/tinymce");

await rm(destination, { recursive: true, force: true });
await mkdir(destination, { recursive: true });

await Promise.all([
  cp(resolve(packageDirectory, "tinymce.min.js"), resolve(destination, "tinymce.min.js")),
  cp(resolve(packageDirectory, "icons"), resolve(destination, "icons"), { recursive: true }),
  cp(resolve(packageDirectory, "models"), resolve(destination, "models"), { recursive: true }),
  cp(resolve(packageDirectory, "plugins"), resolve(destination, "plugins"), { recursive: true }),
  cp(resolve(packageDirectory, "skins"), resolve(destination, "skins"), { recursive: true }),
  cp(resolve(packageDirectory, "themes"), resolve(destination, "themes"), { recursive: true }),
]);
