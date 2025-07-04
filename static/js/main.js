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

// Placeholder: Add a marker at Yukon Bible Church
L.marker([35.5062, -97.7668]).addTo(map)
    .bindPopup('Yukon Bible Church')
    .openPopup();
// Load GeoJSON Fields
fetch('/static/geo/fields.geojson')
    .then(response => response.json())
    .then(geoData => {
        L.geoJSON(geoData, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.name);
            },
            style: {
                color: 'green',
                fillColor: '#7FFF7F',
                fillOpacity: 0.4
            }
        }).addTo(map);
    });
