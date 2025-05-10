function reloadPageRequest() {
    fetch('/github/reload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})  // send an empty JSON object
    })
    .then(response => {
        if (response.ok) {
            console.log("Reload triggered successfully.");
            location.reload();
        } else {
            console.error("Failed to trigger reload.");
        }
    })
    .catch(error => console.error("Error:", error));
}


function reloadPage() {
    const reloadIcon = document.querySelector('.reload-icon');
    reloadIcon.classList.add('spin');


    reloadPageRequest();
    setTimeout(() => {
        reloadIcon.classList.remove('spin');
    }, 2000);
}


function updateTime() {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
    document.getElementById("current-time").textContent = formattedTime;
}


updateTime();
setInterval(updateTime, 1000);
