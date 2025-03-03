async function fetchWeather() {


    const keyResponse = await fetch("/weather/key");
    const keyData = await keyResponse.json();


    if (!keyData.apiKey) {
        throw new Error("Failed to get API key");
    }

    const apiKey = keyData.apiKey;
    const city = "Utrecht, NL";

    try {

        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`);

        const data = await response.json();

        if (data.cod !== 200) {
            throw new Error(data.message);
        }

        const weather_temperature = Math.round(data.main.temp);
        const feelsLike = Math.round(data.main.feels_like);
        const cityName = data.name;
        const sunrise = new Date(data.sys.sunrise * 1000).toLocaleTimeString("en-GB", {
            hour: "2-digit",
            minute: "2-digit"
        });
        const sunset = new Date(data.sys.sunset * 1000).toLocaleTimeString("en-GB", {
            hour: "2-digit",
            minute: "2-digit"
        });

        // Update the DOM
        document.getElementById("city").textContent = cityName;
        document.getElementById("weather_temperature").innerHTML = `${weather_temperature}°C <span class="text-sm text-gray-400">(Feels like ${feelsLike}°C)</span>`;
        document.getElementById("sunrise").textContent = sunrise;
        document.getElementById("sunset").textContent = sunset;
    } catch (error) {
        console.error("Error fetching weather data:", error);
        document.getElementById("city").textContent = "Weather data unavailable";
        document.getElementById("weather_temperature").innerHTML = "--°C (Feels like --°C)";
        document.getElementById("sunrise").textContent = "--:--";
        document.getElementById("sunset").textContent = "--:--";
    }
}

fetchWeather();
setInterval(fetchWeather, 180000);