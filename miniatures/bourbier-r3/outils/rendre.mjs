// Rend une page HTML de miniature en PNG 1280×720.
// Usage : node outils/rendre.mjs index.html rendus/miniature.png   (depuis le dossier de la miniature)
// puis : ffmpeg -i rendus/miniature.png -q:v 2 rendus/miniature-bourbier-r3.jpg   (JPG < 2 Mo pour YouTube)
import { resolve } from "node:path";
import puppeteer from "puppeteer-core";

const [page_html, sortie] = process.argv.slice(2);
const navigateur = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--no-sandbox"] });
const page = await navigateur.newPage();
await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
await page.goto("file://" + resolve(page_html), { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => window.ajuster && window.ajuster());
const absentes = await page.evaluate(() => [...document.fonts].filter(f => f.status === "error").map(f => f.family));
if (absentes.length) { console.error("polices non chargées :", absentes); process.exit(1); }
await page.screenshot({ path: sortie });
await navigateur.close();
console.log("rendu :", sortie);
