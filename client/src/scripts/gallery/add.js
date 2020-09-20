import {mediaContainer} from "./mediaContainer";

export function addVideo(video) {
  let videoElement = document.createElement('video');
  videoElement.classList.add('multimedia');

  let sourceElement = document.createElement('source');
  sourceElement.setAttribute('src', video.url);

  videoElement.appendChild(sourceElement);
  mediaContainer.element.appendChild(videoElement);
  sourceElement.play();
}

export function addImage(image) {
  let imageElement = document.createElement('div');
  imageElement.classList.add('multimedia');

  let sourceElement = document.createElement('img');
  sourceElement.setAttribute('src', image.url);

  imageElement.appendChild(sourceElement);
  mediaContainer.element.appendChild(imageElement);
}
