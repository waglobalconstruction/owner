// Usage: node render.js IN.html OUT.png SCALE [transparent]
const { chromium } = require('playwright');
(async () => {
  const [inp, out, scale, transp] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: Number(scale || 1) });
  await page.goto('file://' + inp);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const el = await page.$('#art');
  await el.screenshot({ path: out, omitBackground: transp === 'transparent' });
  await browser.close();
  console.log('saved', out);
})();
