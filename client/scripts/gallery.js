const multimediaContainer = document.querySelector('#multimedia-container');

var Gallery = {
    currentMedia: 0,
    gallery: document.querySelector('#gallery'),

    addVideo: (video) => {
        let videoElement = document.createElement('video');
        videoElement.classList.add('multimedia');

        let sourceElement = document.createElement('source');
        sourceElement.setAttribute('src', video.url);

        videoElement.appendChild(sourceElement);
        multimediaContainer.appendChild(videoElement);
    },
    addImage: (image) => {
        let imageElement = document.createElement('div');
        imageElement.classList.add('multimedia');

        let sourceElement = document.createElement('img');
        sourceElement.setAttribute('src', image.url);

        imageElement.appendChild(sourceElement);
        multimediaContainer.appendChild(imageElement);
    },
    idFromLocation: (loc) => {
        let precision = 2;
        let result = 'loc';
        [loc.lat, loc.lng].forEach((x) => {
            x = Number(x).toFixed(precision);
            result += String(x).replace('.', '');
        });
        return result;
    }
}

function showGallery(e){
    let galleryId = Gallery.idFromLocation(e.latlng);
    MediaStorage.toGallery(e.latlng);

    let map = document.querySelector('#mapid');
    map.style.opacity = '60%';

    let multimedia = multimediaContainer.querySelectorAll('.multimedia');
    Gallery.gallery.style.display = 'flex';
    Gallery.gallery.style['z-index'] = 2;
}

function closeGallery() {
    let map = document.querySelector('#mapid');
    Gallery.gallery.style['z-index'] = 0;
    map.style.opacity = null;
}
