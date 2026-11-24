// Gentle scroll-reveal for cards and sections
(function(){
  var els=document.querySelectorAll('.card,.t,.cta,.band,.art>h2,.art ol,.art blockquote,.pinimg,ul.chk li,.toc,.tip');
  els.forEach(function(e,i){e.classList.add('reveal');e.style.transitionDelay=((i%3)*90)+'ms';});
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:.12});
  els.forEach(function(e){io.observe(e)});
})();

// Article filters (articles.html)
(function(){
  var bar=document.querySelector('.filters');if(!bar)return;
  bar.addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;var f=b.getAttribute('data-f');
    bar.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});
    document.querySelectorAll('.cards .card').forEach(function(c){c.hidden=!(f==='all'||c.getAttribute('data-guide')===f);c.classList.add('in')});
  });
})();
