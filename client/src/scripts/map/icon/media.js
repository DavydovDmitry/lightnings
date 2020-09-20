import {backgroundStyle} from "./background";
import Icon from "ol/style/Icon";
import {Style} from "ol/style";
import mediaImage from "../../../images/media-icon.svg";
import videoImage from "../../../images/video-icon.svg";
import imageImage from "../../../images/image-icon.svg";

const scale = 0.14;

export const videoIconStyle = [
  backgroundStyle,
  new Style({
    image: new Icon({
      src: videoImage,
      scale: scale
    })
  })
];

export const imageIconStyle = [
  backgroundStyle,
  new Style({
    image: new Icon({
      src: imageImage,
      scale: scale
    })
  })
];

export const mediaIconStyle = [
  backgroundStyle,
  new Style({
    image: new Icon({
      src: mediaImage,
      scale: scale
    })
  })
];
