import {REST_PROTOCOL, REST_IP, REST_PORT} from "./config";
import {idFromLonLat} from "./locationId"
import {worldMap, videoIconStyle, imageIconStyle, MediaFeature} from './map';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import {MediaStorage} from "./mediaStorage";

export function loadMeteo(){
  const xhr = new XMLHttpRequest();
  xhr.open('GET', `${REST_PROTOCOL}://${REST_IP}:${REST_PORT}/meteo`);
  xhr.onload = async (evt) => {
    await MediaStorage.createObjectStores();
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
    videoLocations.forEach((value) => {
      mapFeatures.push(new MediaFeature(value.lon, value.lat, videoIconStyle));
    })
    imageLocations.forEach((value, key) => {
      mapFeatures.push(new MediaFeature(value.lon, value.lat, imageIconStyle));
    })
    mediaLocations.forEach((value) => {
      mapFeatures.push(new MediaFeature(value.lon, value.lat));
    })

    worldMap.addLayer(new VectorLayer({
      source: new VectorSource({
        features: mapFeatures
      })
    }));
  };
  xhr.send();
}
