const { chromium } = require('playwright');
const fs = require('fs');
const OUT = __dirname + '/../out/raw';
const JOBS = [
  { svg: 'gemis-studio-lockup.svg',        out: 'logo-lockup',        w: 1024, h: 262 },
  { svg: 'gemis-studio-lockup-light.svg',  out: 'logo-lockup-light',  w: 1024, h: 262 },
  { svg: 'gemis-studio-stacked.svg',       out: 'logo-stacked',       w: 600,  h: 622 },
  { svg: 'gemis-studio-stacked-light.svg', out: 'logo-stacked-light', w: 600,  h: 622 },
  { svg: 'gemis-studio-mark.svg',          out: 'logo-mark',          w: 512,  h: 419 },
  { svg: 'gemis-studio-mark-light.svg',    out: 'logo-mark-light',    w: 512,  h: 419 },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const j of JOBS) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 2 });
    await p.setContent(`<style>html,body{margin:0;background:transparent}
      img{display:block;width:${j.w}px;height:${j.h}px}</style>
      <img src="file://${__dirname}/../logo/${j.svg}">`);
    await p.waitForTimeout(250);
    await p.screenshot({ path: `${OUT}/${j.out}@2x.png`, omitBackground: true });
    await p.close();
    console.log(`${j.out}  ${j.w}x${j.h}`);
  }
  await b.close();
})();
