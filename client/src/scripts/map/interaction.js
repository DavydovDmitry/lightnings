import {worldMap} from "./worldMap";

let selected;

worldMap.on('pointermove', (event) => {
  selected = worldMap.getFeaturesAtPixel(event.pixel)[0];
  if (selected !== undefined){
    worldMap.getTargetElement().style.cursor = 'pointer';
    // console.log(selected)
  } else {
    worldMap.getTargetElement().style.cursor = '';
  }
})

worldMap.on('click', (event) => {
  let f = worldMap.getFeaturesAtPixel(event.pixel);
  console.log(f);
})
