const galleryContainer = document.querySelector('#gallery-container');

class Gallery {
    constructor(multimedia){
        this.gallery = this.getGallery(multimedia);
    }
    addVideo(video){
        let videoElement = document.createElement('video');
        videoElement.classList.add('multimedia');

        let sourceElement = document.createElement('source');
        sourceElement.setAttribute('src', video.url);

        videoElement.appendChild(sourceElement);
        this.gallery.appendChild(videoElement);
    }
    addImage(image){
        let imageElement = document.createElement('div');
        imageElement.classList.add('multimedia');

        let sourceElement = document.createElement('img');
        sourceElement.setAttribute('src', image.url);

        imageElement.appendChild(sourceElement);
        this.gallery.appendChild(imageElement);
    }
    static idFromLocation(loc){
        let precision = 2;
        let result = 'loc';
        [loc.lat, loc.lng].forEach((x) => {
            x = Number(x).toFixed(precision);
            result += String(x).replace('.', '');
        });
        return result;
    }
    getGallery(multimedia){
        let galleryId= Gallery.idFromLocation({
            lat: multimedia.lat,
            lng: multimedia.lng
        });
        let gallery = document.querySelector(`#${galleryId}`);
        if (gallery === null) {
            gallery = document.createElement('div',);
            gallery.classList.add('gallery');
            gallery.id = galleryId;
            galleryContainer.appendChild(gallery);
        }
        return gallery;
    }
}

function showGallery(e){
    let galleryId = Gallery.idFromLocation(e.latlng);
    let gallery = galleryContainer.querySelector(`#${galleryId}`);
    let map = document.querySelector('#mapid');
    map.style['z-index'] = 0;
    gallery.style.display = 'block';
}
