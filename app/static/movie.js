const results = document.querySelector("#result-container");
const sendButton = document.querySelector("#submit-button");
const emotionInput = document.querySelector("#emotion");

function createMovieCard(movie) {
    const result = document.createElement("article");
    result.className = "result";

    const poster = document.createElement("div");
    poster.className = "poster";

    const image = document.createElement("img");
    image.id = "movie_image";
    image.alt = movie.title || movie.original_title || "Movie poster";
    image.src = movie.poster_path
        ? `https://image.tmdb.org/t/p/w500/${movie.poster_path}`
        : "https://placehold.co/400x600/e7e7e7/1d3342?text=No+Poster";

    const about = document.createElement("div");
    about.id = "about";

    const title = document.createElement("div");
    title.className = "title-line";
    title.textContent = movie.original_title || movie.title || "Untitled";

    const meta = document.createElement("div");
    meta.className = "meta-row";

    const language = document.createElement("span");
    language.className = "meta-pill";
    language.textContent = `Language: ${(movie.original_language || "N/A").toUpperCase()}`;

    const rating = document.createElement("span");
    rating.className = "meta-pill";
    rating.textContent = `Rating: ${movie.vote_average ?? "N/A"}`;

    const overview = document.createElement("div");
    overview.textContent = movie.overview || "No description available for this recommendation.";

    meta.appendChild(language);
    meta.appendChild(rating);
    about.appendChild(title);
    about.appendChild(meta);
    about.appendChild(overview);
    poster.appendChild(image);
    result.appendChild(poster);
    result.appendChild(about);

    return result;
}

async function searchMovies() {
    const prompt = emotionInput.value.trim();
    results.innerHTML = "";

    if (!prompt) {
        results.innerHTML = "<p>Please describe how you feel first.</p>";
        return;
    }

    sendButton.disabled = true;
    sendButton.textContent = "Searching...";

    try {
        const response = await fetch("/get_movie", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ Feeling: prompt })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Unable to fetch movies right now.");
        }

        const movies = Array.isArray(data.results) ? data.results.slice(0, 8) : [];
        if (!movies.length) {
            results.innerHTML = "<p>No recommendations found for that feeling yet.</p>";
            return;
        }

        movies.forEach((movie) => {
            results.appendChild(createMovieCard(movie));
        });
    } catch (error) {
        results.innerHTML = `<p>${error.message}</p>`;
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Find movies";
    }
}

sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    searchMovies();
});

emotionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        searchMovies();
    }
});
