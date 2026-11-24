// usage: node animate.js pin.html out.mp4 [seconds=8] [width=1080] [height=1920] [fps=30]
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),{execSync}=require('child_process');
(async()=>{const [,,src,out,sec='8',w='1080',h='1920',fps='30']=process.argv;
const dir=fs.mkdtempSync('/tmp/frames-');const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
await p.goto('file://'+path.resolve(src));await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>document.getAnimations().forEach(a=>a.pause()));
const n=Math.round(+sec*+fps);
for(let i=0;i<n;i++){const t=i*1000/+fps;
 await p.evaluate(t=>document.getAnimations().forEach(a=>a.currentTime=t),t);
 await p.screenshot({path:`${dir}/f${String(i).padStart(5,'0')}.png`});}
await b.close();
execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${dir}/f%05d.png -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart ${out}`);
fs.rmSync(dir,{recursive:true});console.log('wrote',out,n,'frames');})();
