import {REST_PROTOCOL, REST_IP, REST_PORT} from "./config";
import {map, iconStyle} from './map';
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
    let markerFeatures = [];

    data['videos'].forEach(video => {
      let videoFeature = new Feature({
                 geometry: new Point(fromLonLat([video.lng, video.lat]))
             });
      videoFeature.setStyle(iconStyle);
      markerFeatures.push(videoFeature);
      MediaStorage.addVideo(video);
      // marker.on('click', Gallery.show);
    });

    data['images'].forEach(image => {
      let imageFeature = new Feature({
        geometry: new Point(fromLonLat([image.lng, image.lat]))
      });
      imageFeature.setStyle(iconStyle);
      markerFeatures.push(imageFeature);
      MediaStorage.addImage(image);
      // marker.on('click', Gallery.show);
    });

    map.addLayer(new VectorLayer({
      source: new VectorSource({
        features: markerFeatures
      })
    }));
  };
  xhr.send();
}
