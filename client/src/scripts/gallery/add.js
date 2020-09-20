import {REST_PROTOCOL, REST_IP, REST_PORT} from "../config";
import {mediaContainer} from "./mediaContainer";

export function addVideo(video) {
  let videoElement = document.createElement('video');
  videoElement.classList.add('multimedia');
  videoElement.setAttribute('controls', '')
  videoElement.setAttribute('autoplay', '');
  videoElement.setAttribute('width', '100%');

  let sourceElement = document.createElement('source');
  sourceElement.setAttribute('src', `${REST_PROTOCOL}://${REST_IP}:${REST_PORT}/media/${video.url}`);

  videoElement.appendChild(sourceElement);
  mediaContainer.element.appendChild(videoElement);
}

export function addImage(image) {
  let imageElement = document.createElement('div');
  imageElement.classList.add('multimedia');

  let sourceElement = document.createElement('img');
  sourceElement.setAttribute('src', image.url);

  imageElement.appendChild(sourceElement);
  mediaContainer.element.appendChild(imageElement);
}
