// Get weather + OEAI
fetch('/api/weather')
    .then(response => response.json())
    .then(data => {
        document.getElementById('comfort-message').innerText = data.comfort_message;
        document.getElementById('temp').innerText = data.temp_f;
        document.getElementById('humidity').innerText = data.humidity;
        document.getElementById('wind').innerText = data.wind_speed;
        document.getElementById('cloud').innerText = data.cloud_cover;
    });

// Create Leaflet map
const map = L.map('map').setView([35.5062, -97.7668], 16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);
L.marker([35.5062, -97.7668]).addTo(map).bindPopup('Yukon Bible Church');

function loadFields() {
  fetch('/static/geo/fields.geojson').then(res => res.json()).then(geo => {
    L.geoJSON(geo, {
      style: { color: '#FF6A00', fillColor: '#FFA84D', fillOpacity: 0.5 },
      onEachFeature: (feat, layer) => layer.bindPopup(feat.properties.name)
    }).addTo(map);
  });
}
loadFields();

function updateWeather() {
  const age = document.getElementById('ageSelect').value;
  fetch(`/api/weather?age_group=${age}`).then(res => res.json()).then(data => {
    document.getElementById('comfort-message').innerText = data.comfort_message;
    document.getElementById('temp').innerText = data.temp_f;
    document.getElementById('humidity').innerText = data.humidity;
    document.getElementById('wind').innerText = data.wind_speed;
    document.getElementById('cloud').innerText = data.cloud_cover;

    const container = document.getElementById('comfort-message-container');
    container.className = 'p-4 rounded text-white text-center text-xl font-bold';

    if (data.oeai >= 80) {
      container.classList.add('bg-green-600');
    } else if (data.oeai >= 60) {
      container.classList.add('bg-yellow-500', 'text-black');
    } else if (data.oeai >= 40) {
      container.classList.add('bg-orange-500');
    } else {
      container.classList.add('bg-red-600');
    }
  });
}

document.getElementById('ageSelect').addEventListener('change', updateWeather);
updateWeather();
