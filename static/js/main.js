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

    const msgEl = document.getElementById('comfort-message');
    msgEl.className = '';
    const score = data.oeai;
    if (score >= 80) {
      msgEl.classList.add('text-green-600');
    } else if (score >= 60) {
      msgEl.classList.add('text-yellow-600');
    } else {
      msgEl.classList.add('text-red-600');
    }
  });
}

document.getElementById('ageSelect').addEventListener('change', updateWeather);
updateWeather();
