import {gsap} from 'gsap';
import {ScrollTrigger} from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
function updateScenes(){
  const marker=innerHeight*.53;
  for(const group of document.querySelectorAll('.country')){
    const steps=Array.from(group.querySelectorAll('.step'));
    const i=Math.max(0,steps.findLastIndex(s=>s.getBoundingClientRect().top<marker));
    const fig=group.querySelector('.artifact');
    const [a,b]=fig.querySelectorAll('.pair span');
    a.textContent=steps[i].dataset.labelA;b.textContent=steps[i].dataset.labelB;
    fig.style.setProperty('--zoom',1+i*.035);fig.dataset.index=i;
  }
  const max=document.documentElement.scrollHeight-innerHeight;
  document.querySelector('#progress').style.transform='scaleX('+Math.min(1,Math.max(0,scrollY/max))+')';
}
const schedule=()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{scheduled=false;updateScenes()})}};let scheduled=false;
addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);updateScenes();
gsap.matchMedia().add('(prefers-reduced-motion: no-preference)',()=>{
 gsap.fromTo('.work-image',{scale:1.015},{scale:1.12,yPercent:1.8,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:true}});
});
const comparisons=[
 ['노사 전문가는 기업훈련규정을, 주 전문가는 학교 교육과정을 준비한다. 연방과 주가 두 문서를 조율한다.','산업계가 능력기준 개발에 참여하고 전국 단위 체계가 훈련·평가의 공통 기준을 조정한다.','연방은 보조금의 사용 조건을 정하고 주는 학교와 교육과정을 포함한 집행 계획을 제출한다.'],
 ['기업은 현장훈련과 훈련수당을, 주는 직업학교 교육을 맡는다. 두 학습 장소의 비용을 서로 다른 주체가 부담한다.','연방과 주·준주가 훈련 재정을 분담한다. 자격이 전국에서 통용돼도 구체적인 지원 조건은 지역과 과정에 따라 다를 수 있다.','1917년 스미스·휴스법에서는 연방 보조금에 주 또는 지방정부가 같은 금액의 재원을 대응 부담했다.'],
 ['기업과 학교에서 익힌 내용을 직업 단위의 종결시험과 연결한다. 관할기관이 시험 운영에 참여한다.','등록기관은 다른 기관이 등록 범위 안에서 발급한 자격과 이수증명을 인정한다. 주·준주 사이에서는 기관의 등록 지위도 인정한다.','교육 이수, 자격, 경력으로 연결되는 경로는 주와 지역의 과정에 따라 달라진다. 연방 보조의 대상과 개인의 자격 인정은 구분해 읽어야 한다.']
];
document.querySelectorAll('[data-q]').forEach(button=>button.addEventListener('click',()=>{
 document.querySelectorAll('[data-q]').forEach(b=>b.setAttribute('aria-pressed',b===button));
 document.querySelectorAll('.compare-grid p').forEach((p,i)=>p.textContent=comparisons[Number(button.dataset.q)][i]);
}));
let viewer;const toggle=document.querySelector('#model-toggle');const status=document.querySelector('#model-status');
toggle.addEventListener('click',async()=>{
 if(viewer){viewer.dispose();viewer=null;toggle.textContent='3D로 살펴보기';toggle.setAttribute('aria-pressed','false');status.textContent='';return;}
 toggle.disabled=true;status.textContent='3D 작업대를 여는 중…';
 try{const {mount}=await import('./viewer.js');viewer=await mount(document.querySelector('#model-stage'),reduce);toggle.textContent='정지 화면 보기';toggle.setAttribute('aria-pressed','true');status.textContent='좌우로 드래그하거나, 모델을 선택하고 방향키를 눌러 살펴보세요.';}
 catch{status.textContent='이 기기에서는 Blender 정지 화면으로 볼 수 있습니다.';}finally{toggle.disabled=false;}
});
