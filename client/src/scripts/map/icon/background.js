import {Fill, Stroke, Circle, Style} from 'ol/style';

const fill = new Fill({
 color: 'rgb(74,154,246)'
});

const stroke = new Stroke({
 color: '#2f48c6',
 width: 2
});

export const backgroundStyle = new Style({
  image: new Circle({
       fill: fill,
       // stroke: stroke,
       radius: 20
     }),
  fill: fill,
});
