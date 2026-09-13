const videoFeed = document.getElementById("video-feed");
const statusText = document.getElementById("status");
let emotionInterval = null;

function setStatus(message) {
    statusText.innerText = message;
}

function startLiveFeed() {
    setStatus("Starting live feed...");

    fetch("/start_feed")
        .then((response) => response.json())
        .then(() => {
            videoFeed.src = "/video_feed";
            setStatus("Feed is live. Stay in frame for a few seconds.");

            if (emotionInterval) {
                clearInterval(emotionInterval);
            }

            emotionInterval = setInterval(() => {
                fetch("/get_emotion")
                    .then((response) => response.json())
                    .then((data) => {
                        setStatus(`Detected emotion: ${data.emotion || "Reading..."}`);
                    })
                    .catch(() => {
                        setStatus("Reading emotion...");
                    });
            }, 1000);
        })
        .catch(() => {
            setStatus("Unable to start the feed right now.");
        });
}

function stopLiveFeed() {
    fetch("/stop_feed")
        .then((response) => response.json())
        .then(() => {
            videoFeed.src = "";
            setStatus("Emotion saved successfully.");

            if (emotionInterval) {
                clearInterval(emotionInterval);
                emotionInterval = null;
            }
        })
        .catch(() => {
            setStatus("Unable to stop the feed right now.");
        });
}
