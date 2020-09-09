const multimediaContainer = document.querySelector('#multimedia-container');

var Gallery = {
    currentMedia: 0,
    map: document.querySelector('#mapid'),
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
    },
    show: (e) => {
        MediaStorage.toGallery(e.latlng);

        let multimedia = multimediaContainer.querySelectorAll('.multimedia');

        Gallery.map.style.opacity = '60%';
        Gallery.gallery.style.display = 'flex';
        Gallery.gallery.style['z-index'] = 2;
    },
    close: () => {
        Gallery.map.style.opacity = null;
        Gallery.gallery.style.display = 'none';
        Gallery.gallery.style['z-index'] = 0;

        multimediaContainer.querySelectorAll('.multimedia').forEach((media) => {
            media.remove();
        })
    }
}
Gallery.gallery.querySelector('header button').addEventListener('click', Gallery.close);
