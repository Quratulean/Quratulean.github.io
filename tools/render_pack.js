// node tools/render_pack.js <dir>  ->  <dir>/ramadan-family-planner-A4.pdf, -Letter.pdf and preview-NN.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const url = 'file://' + dir + '/ramadan-pack.html';
  const b = await chromium.launch();
  for (const [fmt, W, H] of [['A4', '210mm', '297mm'], ['Letter', '215.9mm', '279.4mm']]) {
    const p = await b.newPage();
    await p.goto(url, { waitUntil: 'networkidle' });
    await p.addStyleTag({ content: `:root{--W:${W};--H:${H}}` });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: `${dir}/ramadan-family-planner-${fmt}.pdf`, format: fmt, printBackground: true,
                  margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    if (fmt === 'A4') {
      await p.setViewportSize({ width: 794, height: 1123 });
      const secs = await p.$$('section.page');
      for (let i = 0; i < secs.length; i++) {
        await secs[i].screenshot({ path: `${dir}/preview-${String(i + 1).padStart(2, '0')}.png` });
      }
    }
    await p.close();
  }
  await b.close();
})();
