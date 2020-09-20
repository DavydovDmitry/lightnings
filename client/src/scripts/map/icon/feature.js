import {Feature} from "ol"
import Point from "ol/geom/Point";
import {fromLonLat} from "ol/proj";
import {mediaIconStyle, imageIconStyle, videoIconStyle} from "../icon"
import {idFromLonLat} from "../../locationId"

export class MediaFeature extends Feature{
  constructor(lon, lat, style=mediaIconStyle){
    super({
      geometry: new Point(fromLonLat([lon, lat]))
    });
    this.setStyle(style);
    this.setId(idFromLonLat(lon, lat));
  }
}
