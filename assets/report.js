
const chapters=[...document.querySelectorAll('.report-chapter')],links=[...document.querySelectorAll('nav a')];
let pending=false;
function update(){pending=false;let index=0;const boundary=innerWidth<=700?150:100;chapters.forEach((section,i)=>{if(section.getBoundingClientRect().top<=boundary)index=i});links.forEach((link,i)=>{if(i===index)link.setAttribute('aria-current','page');else link.removeAttribute('aria-current')})}
window.addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(update)}},{passive:true});
window.addEventListener('resize',update);
document.getElementById('print').addEventListener('click',event=>{event.preventDefault();window.print()});
requestAnimationFrame(update);
