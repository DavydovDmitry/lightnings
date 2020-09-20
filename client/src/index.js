import lightningsIcon from './images/logo.ico';
document.getElementById('lightnings-icon').setAttribute('href', lightningsIcon);
import './styles/index.scss';

import "./scripts/mediaStorage";
import "./scripts/gallery";
import {loadMeteo} from "./scripts/loadMeteo";

loadMeteo();
