function addMessage(text, sender){

const chatbox=document.getElementById("chatbox")

const div=document.createElement("div")

div.className=sender

if(sender==="ai"){

div.innerHTML=`
<div style="display:flex;align-items:flex-start;gap:8px">
<div class="ai-avatar"></div>
<span class="bubble"></span>
</div>
`

}else{

div.innerHTML=`<span class="bubble">${text}</span>`

}

chatbox.appendChild(div)

chatbox.scrollTop=chatbox.scrollHeight

if(sender==="ai"){

typeText(div.querySelector(".bubble"),text)

}

}

function typeText(element,text){

let i=0

const speed=20

function typing(){

if(i<text.length){

element.innerHTML+=text.charAt(i)

i++

setTimeout(typing,speed)

}

}

typing()

}

function showTyping(){

const chatbox=document.getElementById("chatbox")

const typing=document.createElement("div")

typing.className="typing"

typing.id="typing"

typing.innerHTML=`
<div class="ai-avatar"></div>
<div style="display:flex;gap:5px">
<div class="dot"></div>
<div class="dot"></div>
<div class="dot"></div>
</div>
`

chatbox.appendChild(typing)

chatbox.scrollTop=chatbox.scrollHeight

}

function sendMessage(){

const input=document.getElementById("message")

const message=input.value.trim()

if(!message) return

addMessage(message,"user")

input.value=""

showTyping()

fetch("/citizen/ai/chat/",{
method:"POST",
headers:{
"Content-Type":"application/x-www-form-urlencoded",
"X-CSRFToken":CSRF_TOKEN
},
body:`message=${message}`
})
.then(res=>res.json())
.then(data=>{

document.getElementById("typing").remove()

addMessage(data.reply,"ai")

})

}

/* ENTER KEY SEND */

document.getElementById("message").addEventListener("keypress",function(e){

if(e.key==="Enter"){

sendMessage()

}

})