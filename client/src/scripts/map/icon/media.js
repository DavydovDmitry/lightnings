import {backgroundStyle} from "./background";
import Icon from "ol/style/Icon";
import {Style} from "ol/style";
import mediaImage from "../../../images/media-icon.svg";

const mediaIcon = new Icon({
  src: mediaImage,
  scale: 0.14
})

export const mediaIconStyle = [
  backgroundStyle,
  new Style({
    image: mediaIcon
  })]
;
