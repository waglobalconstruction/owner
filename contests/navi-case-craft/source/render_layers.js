// Usage: node render_layers.js DIR  -> renders DIR/{paint,spray,stickers}.html to transparent PNGs (2393x1481)
const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const browser = await chromium.launch();
  const [vw, vh] = (process.env.VIEW || '2393x1481').split('x').map(Number);
  const page = await browser.newPage({ viewport: { width: vw, height: vh }, deviceScaleFactor: 1 });
  for (const name of (process.argv[3] || 'paint,spray,stickers').split(',')) {
    await page.goto('file://' + dir + '/' + name + '.html');
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(250);
    const el = await page.$('#art');
    await el.screenshot({ path: dir + '/' + name + '.png', omitBackground: true });
  }
  await browser.close();
  console.log('layers ok');
})();
