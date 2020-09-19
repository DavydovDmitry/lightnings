import Style from "ol/style/Style";
import Icon from "ol/style/Icon";
import videoIcon from '../../images/video-icon.svg'

export const iconStyle = new Style({
  image: new Icon({
    anchorXUnits: 'fraction',
    anchorYUnits: 'pixels',
    src: videoIcon,
    scale: 0.15
  }),
});
