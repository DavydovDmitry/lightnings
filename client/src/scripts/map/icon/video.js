import {backgroundStyle} from "./background";
import Icon from "ol/style/Icon";
import {Style} from "ol/style";
import videoImage from "../../../images/video-icon.svg";

const videoIcon = new Icon({
  // anchorXUnits: 'fraction',
  // anchorYUnits: 'pixels',
  src: videoImage,
  scale: 0.15
})

export const iconStyle = [
  backgroundStyle,
  new Style({
    image: videoIcon
  })]
;
