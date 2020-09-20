import {MediaStorage} from "../mediaStorage"
import {addImage, addVideo} from "./add"
import {navButtons} from "./navButtons"
import {mediaContainer} from "./mediaContainer"

export let Gallery = {
  map: document.querySelector('#map-id'),
  gallery: document.querySelector('#gallery'),

  navButtons: navButtons,

  open: async (id) => {
    let images = await MediaStorage.getImagesByGalleryId(id);
    images.forEach((image) => {
      addImage(image);
    })

    mediaContainer.showFirst();
    if (!mediaContainer.isLastActive()){
      Gallery.navButtons.right.activate()
    }

    Gallery.map.style.opacity = '60%';
    Gallery.gallery.style.display = 'flex';
    Gallery.gallery.style['z-index'] = 2;
  },

  close: () => {
    Gallery.map.style.opacity = null;
    Gallery.gallery.style.display = 'none';
    Gallery.gallery.style['z-index'] = 0;

    mediaContainer.removeAllMedia();
  },
  next: () => {
    mediaContainer.showNext();

    if (!mediaContainer.isFirstActive()){
      Gallery.navButtons.left.activate();
    }
    if (mediaContainer.isLastActive()){
      Gallery.navButtons.right.deactivate();
    }
  },
  prev: () => {
    mediaContainer.showPrev();

    if (mediaContainer.isFirstActive()){
      Gallery.navButtons.left.deactivate();
    }
    if (!mediaContainer.isLastActive()){
      Gallery.navButtons.right.activate();
    }
  }
}


// add event handlers
Gallery.gallery.querySelector('header button').addEventListener('click', Gallery.close);
Gallery.navButtons.left.element.addEventListener('click', Gallery.prev);
Gallery.navButtons.right.element.addEventListener('click', Gallery.next);

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
