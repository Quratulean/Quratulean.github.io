// Renders the HTML files listed in a jobs.json (made by tools/featured.py) to JPG images.
const {chromium} = require('playwright');
(async () => {
  const jobs = require(require('path').resolve(process.argv[2]));
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({viewport: {width: j.w, height: j.h}, deviceScaleFactor: 1});
    await p.goto('file://' + j.src, {waitUntil: 'networkidle'});
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({path: j.out, type: 'jpeg', quality: 86});
    await p.close();
  }
  await b.close();
})();
