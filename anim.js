// Gentle scroll-reveal for cards and sections
(function(){
  var els=document.querySelectorAll('.card,.t,.cta,.band,h2,.art p,.art ol,.art blockquote,.pinimg,ul.chk li');
  els.forEach(function(e,i){e.classList.add('reveal');e.style.transitionDelay=((i%3)*90)+'ms';});
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:.12});
  els.forEach(function(e){io.observe(e)});
})();
