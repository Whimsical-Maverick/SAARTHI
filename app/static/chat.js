const sendbutton = document.querySelector('#submit')
const container = document.querySelector('.chat-body')
sendbutton.addEventListener('click',(e)=>{
    if(e.type=="click")
    {
        e.preventDefault()
        const input_value = document.getElementById('input')
        const input = input_value.value
        const user_input = document.createElement('div')
        user_input.className='user_input'
        user_input.innerText=input
        container.appendChild(user_input)
        input_value.value = ""
        container.scrollTop = container.scrollHeight;
        fetch('/BuddyBot',{
            method : 'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'Input':input})
        })
        .then(response => response.json())
        .then(data=>{
            const gemini_response = document.createElement('div')
            gemini_response.className='message-bubble'
            container.appendChild(gemini_response)
            container.scrollTop = container.scrollHeight;
            gemini_response.innerText=data.message
        })
    }

})