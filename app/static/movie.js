const results = document.querySelector('#result-container')
const send_button = document.querySelector('#submit-button')

send_button.addEventListener('click',(e)=>{
    e.preventDefault()
    const input = document.querySelector('#emotion')
    const prompt = input.value
    fetch('/get_movie',{
        method : 'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body : JSON.stringify({'Feeling':prompt})
    })
    .then(response=>response.json())
    .then(data=>{
        for (let movie of data.results) {
            const result = document.createElement('div');
            result.className = "result";

            const poster = document.createElement('div');
            poster.className = 'poster';

            const image = document.createElement('img');
            image.src = `https://image.tmdb.org/t/p/w500/${movie.poster_path}`;
            image.alt = movie.title;
            image.id = "movie_image"
            const about = document.createElement('div')
            about.id = "about"
            const title = document.createElement('div')
            const lang =  document.createElement('div')
            const desc =  document.createElement('div')
            title.innerHTML=`<b>TITLE - </b>${movie.original_title}`
            lang.innerHTML=`<b>LANGUAGE - </b>${movie.original_language}`
            desc.innerHTML=`<b>DESCRIPTION - </b>${movie.overview}`
            about.appendChild(title)
            about.appendChild(lang)
            about.appendChild(desc)
            poster.appendChild(image)
            result.appendChild(poster)
            result.appendChild(about)
            results.appendChild(result)
        }
    })
})