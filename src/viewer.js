import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
export async function mount(host,reduce){
 const model=await new GLTFLoader().loadAsync(new URL('assets/workshop.glb',document.baseURI).href);
 const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:'low-power'});
 const scene=new THREE.Scene();scene.background=new THREE.Color(0x213840);scene.add(model.scene);
 const pm=new THREE.PMREMGenerator(renderer),room=new RoomEnvironment(),env=pm.fromScene(room,.04);
 scene.environment=env.texture;scene.environmentIntensity=1.15;
 renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.16;renderer.setPixelRatio(Math.min(devicePixelRatio,1.65));
 const key=new THREE.DirectionalLight(0xffe8c7,2.1);key.position.set(2,5,-3);scene.add(key);
 const ground=new THREE.Mesh(new THREE.PlaneGeometry(50,50),new THREE.MeshStandardMaterial({color:0x243a43,roughness:.65}));ground.rotation.x=-Math.PI/2;ground.position.y=-.012;scene.add(ground);
 const camera=new THREE.PerspectiveCamera(37,1,.1,70),el=renderer.domElement;
 el.tabIndex=0;el.setAttribute('role','img');el.setAttribute('aria-label','금속 플랜지 작업대 3D 모형. 좌우 방향키로 시점을 변경할 수 있습니다.');host.append(el);
 let yaw=.46,dx=null,raf=0,visible=true;
 function render(){raf=0;if(!visible)return;const rect=host.getBoundingClientRect();const w=host.clientWidth,h=host.clientHeight;
 renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
 const shift=reduce.matches?0:Math.min(.4,Math.max(0,-rect.top/innerHeight)*.4);
 const r=camera.aspect<1.3?8.1:7.0;camera.position.set(r*Math.sin(yaw+shift),5.5+shift,r*Math.cos(yaw+shift));camera.lookAt(0,.14,0);renderer.render(scene,camera);}
 function request(){if(visible&&!raf)raf=requestAnimationFrame(render);}
 const resize=new ResizeObserver(request);resize.observe(host);const observer=new IntersectionObserver(([e])=>{visible=e.isIntersecting;request()});observer.observe(host);
 function start(e){dx=e.clientX;el.setPointerCapture(e.pointerId);}
 function move(e){if(dx!==null){yaw-=(e.clientX-dx)*.009;dx=e.clientX;request()}}
 el.onpointerdown=start;el.onpointermove=move;el.onpointerup=el.onpointercancel=()=>dx=null;el.onkeydown=e=>{if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();yaw+=e.key==='ArrowRight'?.17:-.17;request()}};
 addEventListener('scroll',request,{passive:true});request();
 return {dispose(){resize.disconnect();observer.disconnect();removeEventListener('scroll',request);cancelAnimationFrame(raf);scene.traverse(o=>{o.geometry?.dispose();if(o.material)for(const m of [].concat(o.material))m.dispose()});env.dispose();room.dispose();pm.dispose();renderer.dispose();el.remove()}}
}
