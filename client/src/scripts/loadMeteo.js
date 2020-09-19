import {REST_PROTOCOL, REST_IP, REST_PORT} from "./config";
import {worldMap, videoIconStyle, idFromLonLat, imageIconStyle, mediaIconStyle} from './map';
import {Feature} from "ol";
import Point from "ol/geom/Point";
import {fromLonLat} from "ol/proj";
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import {MediaStorage} from "./mediaStorage";
import {Gallery} from "./gallery";

export function loadMeteo(){
  const xhr = new XMLHttpRequest();
  xhr.open('GET', `${REST_PROTOCOL}://${REST_IP}:${REST_PORT}/meteo`);
  xhr.onload = async (evt) => {
    await MediaStorage.createStores();
    let data = JSON.parse(evt.target.response);

    let videoLocations = new Map();
    let imageLocations = new Map();

    data['videos'].forEach(video => {
      let id = idFromLonLat(video.lon, video.lat);
      if (!videoLocations.has(id)) videoLocations.set(id, {
        lon: video.lon,
        lat: video.lat
      });
      MediaStorage.addVideo(video);
    });

    data['images'].forEach(image => {
      let id = idFromLonLat(image.lon, image.lat);
      if (!imageLocations.has(id)) imageLocations.set(id, {
        lon: image.lon,
        lat: image.lat
      });
      MediaStorage.addImage(image);
    });

    let mediaLocations = new Map();
    for (let id of videoLocations.keys()){
      if (imageLocations.has(id)){
        mediaLocations.set(id, videoLocations.get(id));
        videoLocations.delete(id);
        imageLocations.delete(id);
      }
    }

    let mapFeatures = [];
    videoLocations.forEach((value, key) => {
      let f = new Feature({
        geometry: new Point(fromLonLat([value.lon, value.lat]))
      })
      f.setStyle(videoIconStyle);
      f.setId(key);
      mapFeatures.push(f);
    })
    imageLocations.forEach((value, key) => {
      let f = new Feature({
        geometry: new Point(fromLonLat([value.lon, value.lat]))
      })
      f.setStyle(imageIconStyle);
      f.setId(key);
      mapFeatures.push(f);
    })
    mediaLocations.forEach((value, key) => {
      let f = new Feature({
        geometry: new Point(fromLonLat([value.lon, value.lat]))
      })
      f.setStyle(mediaIconStyle);
      f.setId(key);
      mapFeatures.push(f);
    })

    worldMap.addLayer(new VectorLayer({
      source: new VectorSource({
        features: mapFeatures
      })
    }));
  };
  xhr.send();
}
