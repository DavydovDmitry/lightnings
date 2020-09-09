var MediaStorage = {
    dbName: 'lightnings',
    dbVersion: 5,

    addVideo: function(video){
        const galleryId = Gallery.idFromLocation({
            lat: video.lat,
            lng: video.lng
        });
        const request = indexedDB.open(MediaStorage.dbName, MediaStorage.dbVersion);
        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            const store = db.createObjectStore('video', {
                keyPath: 'url'
            });
            store.createIndex('galleryId', 'galleryId', {unique: false});
        }
        request.onsuccess = (e) => {
            const db = e.target.result;
            const tx = db.transaction('video', 'readwrite');
            const store = tx.objectStore('video');
            const request = store.add({
                url: video.url,
                galleryId: galleryId
            });
        }
    },
    addImage: function(image){
        const galleryId = Gallery.idFromLocation({
            lat: image.lat,
            lng: image.lng
        });
        const request = indexedDB.open(MediaStorage.dbName, MediaStorage.dbVersion);
        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            const store = db.createObjectStore('image', {
                keyPath: 'url'
            });
            store.createIndex('galleryId', 'galleryId', {unique: false});
        }
        request.onsuccess = (e) => {
            const db = e.target.result;
            const tx = db.transaction('image', 'readwrite');
            const store = tx.objectStore('image');
            const request = store.add({
                url: image.url,
                galleryId: galleryId
            });
        }
    },
    toGallery: function (loc){
        const galleryId = Gallery.idFromLocation(loc);
        const request = window.indexedDB.open(this.dbName, this.dbVersion)
        request.onsuccess = (e) => {
            const db = e.target.result;

            let tx = db.transaction('video', 'readonly');
            let store = tx.objectStore('video');
            let index = store.index('galleryId');
            let videoRequest = index.getAll(IDBKeyRange.only(galleryId));
            videoRequest.onsuccess = (media) => {
                videoRequest.result.forEach((media) => {
                    Gallery.addVideo(media)
                });
            }

            tx = db.transaction('image', 'readonly');
            store = tx.objectStore('image');
            index = store.index('galleryId');
            let imageRequest = index.getAll(IDBKeyRange.only(galleryId));
            imageRequest.onsuccess = (media) => {
                imageRequest.result.forEach((media) => {
                    Gallery.addImage(media)
                });
            }
        }
    }
}
