document.documentElement.classList.add('js');
const nav=document.querySelector('.nav');
addEventListener('scroll',()=>nav.classList.toggle('scrolled',scrollY>8),{passive:true});
const b=document.querySelector('.burger'),m=document.querySelector('.menu');
b?.addEventListener('click',()=>{const o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
/* Escape closes the phone menu and returns focus to the button */
addEventListener('keydown',e=>{if(e.key==='Escape'&&m&&m.classList.contains('open')){m.classList.remove('open');b.setAttribute('aria-expanded','false');b.focus()}});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

/* live RUB -> USD for the English site */
const usdEls=document.querySelectorAll('.usd');
if(usdEls.length){
  const fmt=(rub,rate)=>{const u=rub/rate,s=u<100?5:10;return '$'+Math.max(s,Math.round(u/s)*s).toLocaleString('en-US')};
  const apply=rate=>usdEls.forEach(el=>{el.textContent=fmt(+el.dataset.rub,rate);el.title='≈ '+(+el.dataset.rub).toLocaleString('en-US')+' ₽ at '+rate.toFixed(2)+' ₽/$'});
  let c=null;try{c=JSON.parse(localStorage.getItem('usdrate'))}catch(e){}
  if(c&&Date.now()-c.t<43200000)apply(c.r);
  else fetch('https://open.er-api.com/v6/latest/USD').then(r=>r.json()).then(d=>{const r=d&&d.rates&&d.rates.RUB;if(r>0){apply(r);try{localStorage.setItem('usdrate',JSON.stringify({r,t:Date.now()}))}catch(e){}}}).catch(()=>{});
}

/* copy brief template */
const copyText=async t=>{
  try{await navigator.clipboard.writeText(t);return true}catch(e){}
  try{const a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();const ok=document.execCommand('copy');a.remove();return ok}catch(e){return false}
};
document.querySelectorAll('[data-copy]').forEach(btn=>{const t=btn.textContent;btn.addEventListener('click',async()=>{
  const ok=await copyText(btn.dataset.copy);
  btn.textContent=ok?btn.dataset.done:btn.dataset.fail;setTimeout(()=>btn.textContent=t,2500);
})});


/* the little clips in the intro play only while the intro is on screen */
(()=>{const vs=[...document.querySelectorAll('.fly video')],sc=document.querySelector('.scene');
  if(!vs.length||!sc)return;
  /* if a phone refuses to play a clip (Low Power Mode, data saver), hide it so the cover image below shows, not a play button */
  const drop=v=>{v.hidden=true};
  vs.forEach(v=>v.addEventListener('error',()=>drop(v)));
  const play=on=>vs.forEach(v=>{if(v.hidden)return;v.muted=true;if(on){const p=v.play();if(p)p.catch(e=>{if(e&&e.name==='NotAllowedError'||e&&e.name==='NotSupportedError')drop(v)})}else v.pause()});
  if('IntersectionObserver' in window)new IntersectionObserver(es=>play(es[0].isIntersecting)).observe(sc);else play(true);
})();
/* intro: the scattered work drifts a little with the pointer */
(()=>{const sc=document.querySelector('.scene');
  if(!sc||!matchMedia('(pointer:fine)').matches||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  let raf=0;
  sc.addEventListener('pointermove',e=>{const r=sc.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*2-1,y=(e.clientY-r.top)/r.height*2-1;
    cancelAnimationFrame(raf);raf=requestAnimationFrame(()=>{sc.style.setProperty('--mx',x.toFixed(3));sc.style.setProperty('--my',y.toFixed(3))})});
  sc.addEventListener('pointerleave',()=>{sc.style.setProperty('--mx',0);sc.style.setProperty('--my',0)});
})();

/* smooth scrolling (Lenis), as on anubi.io; off for reduced motion */
const still=matchMedia('(prefers-reduced-motion:reduce)').matches;
let lenis=null;
if(window.Lenis&&!still){
  lenis=new Lenis({lerp:.1,wheelMultiplier:1});
  const loop=t=>{lenis.raf(t);requestAnimationFrame(loop)};requestAnimationFrame(loop);
  document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const t=document.querySelector(a.getAttribute('href'));if(t){e.preventDefault();lenis.scrollTo(t,{offset:-20})}}));
}

/* cases reel: a sideways strip; the centre card is large, neighbours step back.
   Only scrollLeft is read per frame and only CSS variables are written, so it stays smooth. */
const initStrip=()=>{const st=document.querySelector('.reel-stage');if(!st)return;
  const cards=[...st.querySelectorAll('.reel-card')],n=cards.length;
  const cur=document.querySelector('.rc-cur'),bar=document.querySelector('.rc-bar i'),btns=[...document.querySelectorAll('.reel-btn')];
  const still=matchMedia('(prefers-reduced-motion:reduce)').matches;
  let centers=[],w=1,tick=0,idx=0;
  const measure=()=>{w=cards[0].offsetWidth||1;centers=cards.map(c=>c.offsetLeft+c.offsetWidth/2)};
  const draw=()=>{tick=0;
    const mid=st.scrollLeft+st.clientWidth/2;let best=0,bd=Infinity;
    for(let i=0;i<n;i++){const d=(centers[i]-mid)/w,a=Math.abs(d);
      if(!still){cards[i].style.setProperty('--d',Math.max(-2,Math.min(2,d)).toFixed(3));cards[i].style.setProperty('--a',Math.min(a,2).toFixed(3))}
      if(a<bd){bd=a;best=i}}
    idx=best;
    if(cur)cur.textContent=String(best+1).padStart(2,'0');
    const max=st.scrollWidth-st.clientWidth;
    if(bar)bar.style.width=(max>0?st.scrollLeft/max*100:0).toFixed(1)+'%';
    btns.forEach(b=>b.disabled=+b.dataset.dir<0?best===0:best===n-1);
  };
  const req=()=>{if(!tick)tick=requestAnimationFrame(draw)};
  const go=i=>{i=Math.max(0,Math.min(n-1,i));st.scrollTo({left:centers[i]-st.clientWidth/2,behavior:still?'auto':'smooth'})};
  btns.forEach(b=>b.addEventListener('click',()=>go(idx+ +b.dataset.dir)));
  st.addEventListener('scroll',req,{passive:true});
  addEventListener('resize',()=>{measure();req()});
  /* drag with the mouse (touch and trackpads scroll natively) */
  let down=false,moved=false,x0=0,l0=0;
  st.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse'||e.button!==0)return;down=true;moved=false;x0=e.clientX;l0=st.scrollLeft});
  addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-x0;if(!moved&&Math.abs(dx)>5){moved=true;st.classList.add('dragging')}if(moved){st.scrollLeft=l0-dx;e.preventDefault()}});
  addEventListener('pointerup',()=>{if(!down)return;down=false;if(moved){st.classList.remove('dragging');go(idx)}});
  st.addEventListener('click',e=>{if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
  st.addEventListener('dragstart',e=>e.preventDefault());
  measure();draw();
};

/* cases reel, desktop: pinned 3D path measured from anubi.io.
   t = card index minus reel position; t>0 waits up-right in depth, t<0 swings out to the left. */
const init3D=()=>{const reel=document.querySelector('.reel'),st=reel&&reel.querySelector('.reel-stage');if(!st)return;
  const cards=[...st.querySelectorAll('.reel-card')],n=cards.length,cur=reel.querySelector('.rc-cur'),bar=reel.querySelector('.rc-bar i');
  reel.classList.add('live');
  const STEP=.9;                       /* screens of scrolling per project */
  let s=1,tick=0;
  const size=()=>{reel.style.height=Math.round(innerHeight*(1+(n-1)*STEP))+'px';s=(cards[0].offsetWidth||864)/864;if(lenis)lenis.resize()};   /* the page just got taller: let Lenis re-measure */
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const draw=()=>{tick=0;
    const r=reel.getBoundingClientRect(),total=reel.offsetHeight-innerHeight;
    const p=clamp(-r.top/total,0,1),pos=p*(n-1);
    for(let i=0;i<n;i++){const t=i-pos,c=cards[i];let x,y,z,ry,rz,o;
      if(t>=0){const k=Math.sin(1.09*t);x=1072*k;y=-165*k;z=-618*t;ry=-.5*Math.min(1,t*.85);rz=.1*Math.min(1,t);o=t>2?clamp(1-(t-2)/.8,0,1):1}
      else{const a=-t;x=-a*(1150+180*a);y=Math.min(280,190*a);z=a*(600-55*a);ry=.55*a+.17*a*a;rz=-(.12*a+.08*a*a);o=a<.5?1:clamp(1-(a-.5)/.6,0,1)}
      c.style.transform=`translate(-50%,-50%) translate3d(${(x*s).toFixed(1)}px,${(y*s).toFixed(1)}px,${(z*s).toFixed(1)}px) rotateY(${ry.toFixed(3)}rad) rotateZ(${rz.toFixed(3)}rad)`;
      c.style.opacity=o.toFixed(3);c.style.visibility=o<.01?'hidden':'visible';
      c.style.setProperty('--cap',clamp(1-Math.abs(t)*2.2,0,1).toFixed(3));
      c.style.pointerEvents=Math.abs(t)<.5?'auto':'none';
    }
    if(cur)cur.textContent=String(Math.round(pos)+1).padStart(2,'0');
    if(bar)bar.style.width=(p*100).toFixed(1)+'%';
  };
  const req=()=>{if(!tick)tick=requestAnimationFrame(draw)};
  size();draw();
  if(lenis)lenis.on('scroll',req);else addEventListener('scroll',req,{passive:true});
  addEventListener('resize',()=>{size();req()});
  /* keyboard: focusing a card brings the reel to it */
  cards.forEach((c,i)=>c.addEventListener('focus',()=>{const y=reel.offsetTop+(reel.offsetHeight-innerHeight)*i/(n-1);lenis?lenis.scrollTo(y,{immediate:true}):scrollTo(0,y)}));
};
/* images and fonts change the page height after load: re-measure once more */
addEventListener('load',()=>{if(lenis)lenis.resize()});
if(document.querySelector('.reel')){
  if(matchMedia('(min-width:900px)').matches&&!still)init3D();else initStrip();
}

/* hand-drawn strokes draw themselves in when they come into view */
(()=>{const s=[...document.querySelectorAll('.sketch-deco')];if(!s.length)return;
  if(!('IntersectionObserver' in window)){s.forEach(e=>e.classList.add('drawn'));return}
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('drawn');io.unobserve(e.target)}}),{threshold:.6});
  s.forEach(e=>io.observe(e));
})();

/* reviews: "Оригинал" opens the original screenshot large (without script the link opens the image itself) */
(()=>{const d=document.querySelector('.rv-dialog');if(!d||!d.showModal)return;
  let img=null;   /* created on first open, so the closed dialog holds no empty image */
  document.querySelectorAll('.rv-orig').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();
    if(!img){img=document.createElement('img');d.appendChild(img)}
    img.src=a.href;img.alt=a.closest('.chat').querySelector('.msgs').innerText.replace(/\s+/g,' ').trim();
    d.showModal();if(lenis)lenis.stop()}));
  d.addEventListener('close',()=>{if(lenis)lenis.start()});
  d.querySelector('.rv-close').addEventListener('click',()=>d.close());
  d.addEventListener('click',e=>{if(e.target===d)d.close()});
})();

/* keyboard users: bring the focused element into view at once (smooth scrolling would lag behind the focus) */
addEventListener('focusin',e=>{const el=e.target;if(!lenis||!el.getBoundingClientRect||el.closest('.reel-card'))return;
  const r=el.getBoundingClientRect();if(r.top<90||r.bottom>innerHeight-20)lenis.scrollTo(el,{immediate:true,offset:-Math.round(innerHeight/3)})});
