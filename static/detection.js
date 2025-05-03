const videoFeed = document.getElementById('video-feed');
const statusText=document.getElementById('status');
function startLiveFeed() {
    alert("FEED_STARTED...PLEASE KEEP LOOKING IN THE CAMERA")
    fetch('/start_feed')
    .then(response => response.json())
    .then(() => {
    videoFeed.src='/video_feed';
    emotion_interval = setInterval(()=>{
    fetch('/get_emotion')
    .then(response => response.json())
    .then(data => {
        statusText.innerText = "Emotion" +" :" + data.emotion;
        })
    .catch(err=>console.error(err));
        },1000)
    })
}

function stopLiveFeed() {
    alert("FEED_STOPPED")
    fetch('/stop_feed')
    .then(response => response.json())
    .then(() => {
        videoFeed.src = '';
        statusText.innerText = "Emotion Saved Successfully"
        if (emotion_interval) 
        {
            clearInterval(emotion_interval);
            emotion_interval = null;
        }
    })
        .catch(err=>console.error(err))
}