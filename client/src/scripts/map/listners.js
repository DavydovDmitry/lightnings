import {worldMap} from "./worldMap";
import {Gallery} from "../gallery";

let selectedFeature;

worldMap.on('pointermove', (event) => {
  selectedFeature = worldMap.getFeaturesAtPixel(event.pixel)[0];
  if (selectedFeature !== undefined){
    worldMap.getTargetElement().style.cursor = 'pointer';
  } else {
    worldMap.getTargetElement().style.cursor = '';
  }
})

worldMap.on('click', async (event) => {
  let feature = worldMap.getFeaturesAtPixel(event.pixel)[0];
  if (feature !== undefined){
    await Gallery.open(feature.getId());
  }
})
