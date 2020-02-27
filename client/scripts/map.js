var bounds = null;
    
var map = L.map(
    'mapid', {
    center: [60.25, 24.8],
    zoom: 5,
    maxBounds: bounds,
    layers: [],
    worldCopyJump: false,
    crs: L.CRS.EPSG3857,
    zoomControl: true,
    });
L.control.scale().addTo(map);

var tile_layer = L.tileLayer(
    'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
    {
    "attribution": null,
    "detectRetina": false,
    "maxNativeZoom": 18,
    "maxZoom": 18,
    "minZoom": 0,
    "noWrap": false,
    "opacity": 1,
    "subdomains": "abc",
    "tms": false
}).addTo(map);
