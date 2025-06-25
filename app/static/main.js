document.addEventListener('DOMContentLoaded', function() {
let div = document.querySelectorAll('.fact-item')
let ans = document.querySelector('.fact-response')
div.forEach(div => {
div.addEventListener('click',()=>{

    if(div.getAttribute('data-number')==="1")
    {
        ans.innerHTML="<b>It’s okay to feel off. You might not be able to explain what’s wrong — and that’s valid. Being here is already a step forward. 💙</b>"
    }

    if(div.getAttribute('data-number')==="2")
    {
        ans.innerHTML="<b>Putting a name to how you feel — sad, angry, overwhelmed — gives you power over it. 🎯Start small. Even “I don’t know” is a real answer.</b>"
    }

    if(div.getAttribute('data-number')==="3")
    {
        ans.innerHTML="<b>You don’t have to “prove” your pain to ask for help. 🤲 You deserve care just as you are — no explanations needed.</b>"
    }

    if(div.getAttribute('data-number')==="4")
    {
        ans.innerHTML="<b>Stress and emotions often show up as headaches, fatigue, or restlessness. 🌀 Listen to your body. It’s telling a story too.</b>"
    }

    if(div.getAttribute('data-number')==="5")
    {
        ans.innerHTML="<b>Not sure what you’re feeling? That’s okay. 🤷 Even a quiet “something’s not right” matters. Start from there.</b>"
    }

    if(div.getAttribute('data-number')==="6")
    {
        ans.innerHTML="<b>Being here, reading this, exploring your feelings — it all counts. 🦋 Small steps are strong steps. Let’s keep going, together.</b>"
    }

})
})
})