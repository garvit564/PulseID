AOS.init({
duration:1000
});

particlesJS("particles-js",{

particles:{

number:{value:25},

color:{value:"#22c55e"},

size:{value:3},

move:{speed:1}

}

});





window.addEventListener("scroll",()=>{

const nav=document.querySelector(".nav-wrapper");

if(window.scrollY>50){

nav.style.background="rgba(2,6,23,0.9)";
nav.style.backdropFilter="blur(20px)";

}else{

nav.style.background="rgba(255,255,255,0.08)";

}

});






