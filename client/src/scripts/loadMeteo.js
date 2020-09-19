import {REST_PROTOCOL, REST_IP, REST_PORT} from "./config";
import {worldMap, iconStyle, idFromLonLat} from './map';
import {Feature} from "ol";
import Point from "ol/geom/Point";
import {fromLonLat} from "ol/proj";
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import {MediaStorage} from "./mediaStorage";
import {Gallery} from "./gallery";
import {getFeature} from "leaflet/src/layer/GeoJSON";

export function loadMeteo(){
  const xhr = new XMLHttpRequest();
  xhr.open('GET', `${REST_PROTOCOL}://${REST_IP}:${REST_PORT}/meteo`);
  xhr.onload = async (evt) => {
    await MediaStorage.createStores();
    let data = JSON.parse(evt.target.response);
    let mediaFeatures = new Map();

    data['videos'].forEach(video => {
      let videoFeature = new Feature({
        geometry: new Point(fromLonLat([video.lon, video.lat]))
      });
      videoFeature.id = idFromLonLat(video.lon, video.lat);
      videoFeature.setStyle(iconStyle);
      if (!mediaFeatures.has(videoFeature.id)) mediaFeatures.set(videoFeature.id, videoFeature);
      MediaStorage.addVideo(video);
    });

    data['images'].forEach(image => {
      let imageFeature = new Feature({
        geometry: new Point(fromLonLat([image.lon, image.lat])),
      });
      imageFeature.id = idFromLonLat(image.lon, image.lat);
      imageFeature.setStyle(iconStyle);
      if (!mediaFeatures.has(imageFeature.id)) mediaFeatures.set(imageFeature.id, imageFeature);
      MediaStorage.addImage(image);
      // marker.on('click', Gallery.show);
    });


    worldMap.addLayer(new VectorLayer({
      source: new VectorSource({
        features: Array.from(mediaFeatures.values())
      })
    }));
  };
  xhr.send();
}
