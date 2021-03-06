import 'ol/ol.css';
import {Map, View} from 'ol';
import {fromLonLat} from 'ol/proj';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';

// Create map with only one layer - tiles of world map
export const worldMap = new Map({
  target: 'map-id',
  layers: [
    new TileLayer({
      source: new OSM()
    })
  ],
  view: new View({
    center: fromLonLat([37, 55]),
    zoom: 4
  })
});
