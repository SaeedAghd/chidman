(function(){
  function initRing(){
    var ring = document.querySelector('.ring');
    if(!ring) return;
    var v = parseFloat(ring.getAttribute('data-score')||'95');
    var el = ring.querySelector('.ring-value');
    var n=0; var step = Math.max(1, Math.round(v/40));
    var t = setInterval(function(){ n+=step; if(n>=v){n=v; clearInterval(t);} el.textContent=n; }, 18);
  }

  function initTOC(){
    var links=[].slice.call(document.querySelectorAll('.toc a'));
    links.forEach(function(a){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var id=a.getAttribute('href');
        var el=document.querySelector(id);
        if(el){ el.scrollIntoView({behavior:'smooth', block:'start'}); }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    initRing();
    initTOC();
  });
})();


