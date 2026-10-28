// Rend une page HTML en PDF A4. Usage : node publications/pdf.mjs publications/CALENDRIER.html publications/CALENDRIER.pdf
import { resolve } from "node:path";
import puppeteer from "puppeteer-core";

const [entree, sortie] = process.argv.slice(2);
const navigateur = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--no-sandbox"] });
const page = await navigateur.newPage();
await page.goto("file://" + resolve(entree), { waitUntil: "load" });
await page.pdf({ path: sortie, format: "A4", printBackground: true, preferCSSPageSize: true });
await navigateur.close();
console.log("pdf :", sortie);
