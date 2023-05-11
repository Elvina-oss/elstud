const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
var map = L.map('map').setView([55.796127, 49.106405], 13);
map.setZoom(12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);
map.fitWorld();

mapboxgl.accessToken = '{{ mapbox_access_token }}';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [{{ center_lng }}, {{ center_lat }}],
    zoom: 12
});

var markers = {{ markers|safe }};
markers.forEach(function(marker) {
    var el = document.createElement('div');
    el.className = 'marker';
    new mapboxgl.Marker(el)
        .setLngLat([marker.lng, marker.lat])
        .setPopup(new mapboxgl.Popup({ offset: