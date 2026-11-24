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
  if(q)q.addEventListener('input',apply);
})();
