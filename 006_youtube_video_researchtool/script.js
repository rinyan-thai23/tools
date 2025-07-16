// You can hardcode the API key here if desired, otherwise leave it as an empty string
const hardcodedApiKey = '';

// Load API key from local storage if available
document.addEventListener('DOMContentLoaded', () => {
    const savedApiKey = localStorage.getItem('youtubeApiKey');
    if (savedApiKey) {
        document.getElementById('api-key').value = savedApiKey;
    }
});

// ISO 8601 Duration to HH:MM:SS format conversion function
function formatDuration(duration) {
    const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/);
    const hours = (match[1] || '0H').slice(0, -1);
    const minutes = (match[2] || '0M').slice(0, -1);
    const seconds = (match[3] || '0S').slice(0, -1);

    return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}:${seconds.padStart(2, '0')}`;
}

document.getElementById('search-button').addEventListener('click', function() {
    const apiKeyField = document.getElementById('api-key');
    const apiKey = hardcodedApiKey || apiKeyField.value;
    const keyword = document.getElementById('keyword').value;
    const channelId = document.getElementById('channel-id').value;
    const maxResults = document.getElementById('max-results').value;

    if (!hardcodedApiKey) {
        localStorage.setItem('youtubeApiKey', apiKey);
    }

    let apiUrl = `https://www.googleapis.com/youtube/v3/search?key=${apiKey}&part=snippet&type=video&maxResults=${maxResults}`;

    if (keyword) {
        apiUrl += `&q=${keyword}`;
    }

    if (channelId) {
        apiUrl += `&channelId=${channelId}`;
    }

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            const urlsTextarea = document.getElementById('video-urls');
            resultsDiv.innerHTML = '';
            urlsTextarea.value = '';

            const videoIds = data.items.map(item => item.id.videoId).join(',');

            return fetch(`https://www.googleapis.com/youtube/v3/videos?key=${apiKey}&id=${videoIds}&part=contentDetails,snippet`);
        })
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            const urlsTextarea = document.getElementById('video-urls');
            let videoUrls = '';

            data.items.forEach(item => {
                const videoId = item.id;
                const title = item.snippet.title;
                const thumbnail = item.snippet.thumbnails.default.url;
                const duration = formatDuration(item.contentDetails.duration);
                const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
                videoUrls += `${videoUrl}\n`;

                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';

                const thumbnailImg = document.createElement('img');
                thumbnailImg.src = thumbnail;

                const titleLink = document.createElement('a');
                titleLink.href = videoUrl;
                titleLink.target = '_blank';
                titleLink.textContent = title;

                const durationSpan = document.createElement('span');
                durationSpan.textContent = `Duration: ${duration}`;

                resultItem.appendChild(thumbnailImg);
                resultItem.appendChild(titleLink);
                resultItem.appendChild(durationSpan);
                resultsDiv.appendChild(resultItem);
            });

            urlsTextarea.value = videoUrls;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
