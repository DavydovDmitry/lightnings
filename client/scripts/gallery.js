// Representation of document gallery element
var Gallery = {
  map: document.querySelector('#mapid'),
  gallery: document.querySelector('#gallery'),
  multimediaContainer: document.querySelector('#multimedia-container'),
  currentMedia: 0,

  addVideo: (video) => {
    let videoElement = document.createElement('video');
    videoElement.classList.add('multimedia');

    let sourceElement = document.createElement('source');
    sourceElement.setAttribute('src', video.url);

    videoElement.appendChild(sourceElement);
    Gallery.multimediaContainer.appendChild(videoElement);
    videoElement.style.display = 'block';
  },
  addImage: (image) => {
    let imageElement = document.createElement('div');
    imageElement.classList.add('multimedia');

    let sourceElement = document.createElement('img');
    sourceElement.setAttribute('src', image.url);

    imageElement.appendChild(sourceElement);
    Gallery.multimediaContainer.appendChild(imageElement);
    imageElement.style.display = 'block';
  },
  idFromLocation: (loc) => {
    let precision = 2;
    let result = 'loc';
    [loc.lat, loc.lng].forEach((x) => {
        x = Number(x).toFixed(precision);
        result += String(x).replace('.', '');
    });
    return result;
  },
  show: (e) => {
    MediaStorage.toGallery(e.latlng).then(() => {
      let multimedia = Gallery.multimediaContainer.querySelectorAll('.multimedia');
      multimedia[0].style.display = 'block';
    })

    Gallery.map.style.opacity = '60%';
    Gallery.gallery.style.display = 'flex';
    Gallery.gallery.style['z-index'] = 2;
  },
  close: () => {
    Gallery.map.style.opacity = null;
    Gallery.gallery.style.display = 'none';
    Gallery.gallery.style['z-index'] = 0;

    Gallery.multimediaContainer.querySelectorAll('.multimedia').forEach((media) => {
        media.remove();
    })
  },
  next: () => {
    Gallery.currentMedia++;
    let multimedia = Gallery.multimediaContainer.querySelectorAll('.multimedia');
    multimedia[Gallery.currentMedia % multimedia.length].style.display = 'block';
  },
  prev: () => {

  }
}

// add event handlers
Gallery.gallery.querySelector('header button').addEventListener('click', Gallery.close);
Gallery.gallery.querySelector('.gallery-button:first-child').addEventListener('click', Gallery.prev);
Gallery.gallery.querySelector('.gallery-button:last-child').addEventListener('click', Gallery.next);
