import {backgroundStyle} from "./background";
import Icon from "ol/style/Icon";
import {Style} from "ol/style";
import imageImage from "../../../images/image-icon.svg";

const imageIcon = new Icon({
  src: imageImage,
  scale: 0.14
})

export const imageIconStyle = [
  backgroundStyle,
  new Style({
    image: imageIcon
  })]
;
