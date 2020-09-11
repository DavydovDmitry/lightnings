var Gallery = {
  map: document.querySelector('#mapid'),
  gallery: document.querySelector('#gallery'),
  multimediaContainer: document.querySelector('#multimedia-container'),
  leftButton: document.querySelector('.gallery-button:first-child'),
  rightButton: document.querySelector('.gallery-button:last-child'),

  addVideo: (video) => {
    let videoElement = document.createElement('video');
    videoElement.classList.add('multimedia');

    let sourceElement = document.createElement('source');
    sourceElement.setAttribute('src', video.url);

    videoElement.appendChild(sourceElement);
    Gallery.multimediaContainer.appendChild(videoElement);
  },
  addImage: (image) => {
    let imageElement = document.createElement('div');
    imageElement.classList.add('multimedia');

    let sourceElement = document.createElement('img');
    sourceElement.setAttribute('src', image.url);

    imageElement.appendChild(sourceElement);
    Gallery.multimediaContainer.appendChild(imageElement);
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

  button: {
    deactivateLeft: () => {
      Gallery.leftButton.classList.remove('active');
    },
    deactivateRight: () => {
      Gallery.rightButton.classList.remove('active');
    },
    activateLeft: () => {
      Gallery.leftButton.classList.add('active');
    },
    activateRight: () => {
      Gallery.rightButton.classList.add('active');
    },
  },

  media: {
    currentIndex: 0,

    show: () => {
      let multimedia = Gallery.multimediaContainer.querySelectorAll('.multimedia');
      multimedia[Gallery.media.currentIndex].style.display = 'flex';
    },
    close: () => {
      let multimedia = Gallery.multimediaContainer.querySelectorAll('.multimedia');
      multimedia[Gallery.media.currentIndex].style.display = 'none';
    }
  },

  show: (e) => {
    MediaStorage.toGallery(e.latlng).then(() => {
      Gallery.media.currentIndex = 0;
      Gallery.media.show();
      if (Gallery.multimediaContainer.childNodes.length > 1){
        Gallery.button.activateRight();
      }
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
    Gallery.media.close()
    Gallery.media.currentIndex++;
    Gallery.media.show();

    if (Gallery.media.currentIndex > 0){
      Gallery.button.activateLeft();
    }
    if (Gallery.media.currentIndex <= Gallery.multimediaContainer.querySelectorAll('.multimedia').length - 1){
      Gallery.button.deactivateRight();
    }
  },
  prev: () => {
    Gallery.media.close();
    Gallery.media.currentIndex--;
    Gallery.media.show();

    if (Gallery.media.currentIndex <= 0){
      Gallery.button.deactivateLeft();
    }
    if (Gallery.media.currentIndex <= Gallery.multimediaContainer.querySelectorAll('.multimedia').length - 1){
      Gallery.button.activateRight();
    }
  }
}

// add event handlers
Gallery.gallery.querySelector('header button').addEventListener('click', Gallery.close);
Gallery.leftButton.addEventListener('click', Gallery.prev);
Gallery.rightButton.addEventListener('click', Gallery.next);

window.addEventListener('keyup', (e) => {
  switch (e.code){
    case 'Escape':
      Gallery.close();
      break;
    case 'KeyQ':
      Gallery.prev();
      break;
    case 'KeyE':
      Gallery.next();
      break;
  }
});
