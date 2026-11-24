// Gentle scroll-reveal for cards and sections
(function(){
  var els=document.querySelectorAll('.card,.t,.cta,.band,.art>h2,.art ol,.art blockquote,.pinimg,ul.chk li,.toc,.tip');
  els.forEach(function(e,i){e.classList.add('reveal');e.style.transitionDelay=((i%3)*90)+'ms';});
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:.12});
  els.forEach(function(e){io.observe(e)});
})();

// Blog search + topic filter (articles.html)
(function(){
  var bar=document.querySelector('.filters'),q=document.getElementById('q'),none=document.getElementById('none');
  if(!bar&&!q)return;var f='all';
  function apply(){var t=q?q.value.trim().toLowerCase():'',n=0;
    document.querySelectorAll('.cards .card').forEach(function(c){
      var ok=(f==='all'||c.getAttribute('data-guide')===f)&&(!t||(c.getAttribute('data-text')||'').indexOf(t)>-1);
      c.hidden=!ok;c.classList.add('in');if(ok)n++;});
    if(none)none.hidden=n>0;}
  if(bar)bar.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;f=b.getAttribute('data-f');
    bar.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});apply();});
  if(q){q.addEventListener('input',apply);try{var u=new URLSearchParams(location.search).get('q');if(u){q.value=u;apply();}}catch(e){}}
})();

// Phone menu, reading progress, back to top, gentle free-gift invite (2026-11)
(function(){
  var b=document.querySelector('.menubtn'),top=document.querySelector('header.top');
  if(b&&top){b.addEventListener('click',function(){var o=top.classList.toggle('open');b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Close menu':'Open menu');});}
  var isPost=!!document.querySelector('.byline');
  var bar=null,up=document.createElement('a');
  up.href='#';up.className='totop';up.setAttribute('aria-label','Back to top');up.textContent='↑';document.body.appendChild(up);
  up.addEventListener('click',function(e){e.preventDefault();window.scrollTo({top:0,behavior:'smooth'});});
  if(isPost){bar=document.createElement('div');bar.className='readbar';document.body.appendChild(bar);}
  var seen=false;try{seen=localStorage.getItem('ip101-gift')==='1'}catch(e){}
  var gift=null;
  if(isPost&&!seen&&!/free-starter-kit|thank-you/.test(location.pathname)){
    gift=document.createElement('aside');gift.className='giftpop';gift.setAttribute('role','dialog');gift.setAttribute('aria-label','Free gift');
    gift.innerHTML='<button class="x" aria-label="Close">×</button><b>A free gift for you, mama</b><p>The Calm Mama Starter Kit: 4 printable cards for gentler, calmer days.</p><a class="btn" href="free-starter-kit.html">Get it free</a>';
    document.body.appendChild(gift);
    gift.querySelector('.x').addEventListener('click',function(){gift.classList.remove('show');try{localStorage.setItem('ip101-gift','1')}catch(e){}gift=null;});
    gift.querySelector('.btn').addEventListener('click',function(){try{localStorage.setItem('ip101-gift','1')}catch(e){}});
  }
  function onScroll(){var h=document.documentElement,p=h.scrollTop/((h.scrollHeight-h.clientHeight)||1);
    up.classList.toggle('show',h.scrollTop>700);if(bar)bar.style.transform='scaleX('+Math.min(1,p)+')';
    if(gift&&p>0.55)gift.classList.add('show');}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
})();
