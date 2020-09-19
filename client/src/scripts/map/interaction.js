import {worldMap} from "./worldMap";
import {Gallery} from "../gallery";

let selected;

worldMap.on('pointermove', (event) => {
  selected = worldMap.getFeaturesAtPixel(event.pixel)[0];
  if (selected !== undefined){
    worldMap.getTargetElement().style.cursor = 'pointer';
  } else {
    worldMap.getTargetElement().style.cursor = '';
  }
})

worldMap.on('click', (event) => {
  let feature = worldMap.getFeaturesAtPixel(event.pixel)[0];
  if (feature !== undefined){
    Gallery.show(feature.getId());
  }
})
