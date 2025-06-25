const results = document.querySelector('#result-container')
const send_button = document.querySelector('#submit-button')

send_button.addEventListener('click',()=>{
    const input = document.querySelector('#emotion')
    const prompt = input.value
    fetch('/get_movie',{
        method : 'POST',
        headers:{
            'Content-Type':'application/json',
            'Authorization': `Bearer ${}`
        },
        body : JSON.stringify({'Feeling':prompt})
    })
    .then(response=>response.json())
    .then(data=>{
        for(let row=0;row<data['response']['results'].length;row++)
        {
            const result = document.createElement('div')
            result.id="result"
            const poster = document.createElement('div')
            poster.id = 'poster'
            const image = document.createElement('img')
            image.src = `https://image.tmdb.org/t/p/w500/${data['response']['results'][row]['poster_path']}`
            image.alt = data['response']['results'][row]['title']
            poster.appendChild(image)
            result.appendChild(poster)
            results.appendChild(result)
        }
    })
})