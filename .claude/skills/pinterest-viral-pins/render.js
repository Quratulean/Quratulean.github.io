// usage: node render.js pin.html out.png [width] [height]
const {chromium}=require('playwright');
(async()=>{const [,,src,out,w='1000',h='1500']=process.argv;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
await p.goto('file://'+require('path').resolve(src));await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>document.getAnimations().forEach(a=>{a.pause();const e=a.effect.getComputedTiming().endTime;a.currentTime=isFinite(e)?e:0}));
await p.screenshot({path:out});await b.close();})();
