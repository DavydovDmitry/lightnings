var MediaStorage = {
  dbName: 'lightnings',
  dbVersion: 1,
  videoStore: 'video',
  imageStore: 'image',

  createStores: async () => {
    let db = await idb.openDB(MediaStorage.dbName, MediaStorage.dbVersion, {
      upgrade(db, oldVersion, newVersion){
        let store;

        if (oldVersion < 1){
         store = db.createObjectStore(MediaStorage.videoStore, {
            keyPath: 'url'
          });
          store.createIndex('galleryId', 'galleryId', {unique: false});

          store = db.createObjectStore(MediaStorage.imageStore, {
            keyPath: 'url'
          });
          store.createIndex('galleryId', 'galleryId', {unique: false});
        } else {
          console.log('Latter db version');
        }
      }
    });
  },
  addVideo: async (video) => {
    const galleryId = Gallery.idFromLocation({
      lat: video.lat,
      lng: video.lng
    });

    const db = await idb.openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction(MediaStorage.videoStore, 'readwrite');
    const store = tx.objectStore(MediaStorage.videoStore);
    await store.add({
      url: video.url,
      galleryId: galleryId
    });
  },
  addImage: async (image) => {
    const galleryId = Gallery.idFromLocation({
        lat: image.lat,
        lng: image.lng
    });

    const db = await idb.openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction(MediaStorage.imageStore, 'readwrite');
    const store = tx.objectStore(MediaStorage.imageStore);
    await store.add({
      url: image.url,
      galleryId: galleryId
    });
  },
  toGallery: async (loc) => {
    const galleryId = Gallery.idFromLocation(loc);
    const db = await idb.openDB(MediaStorage.dbName, MediaStorage.dbVersion);

    let tx = db.transaction(MediaStorage.videoStore, 'readonly');
    let store = tx.objectStore(MediaStorage.videoStore);
    let index = store.index('galleryId');
    let videos = await index.getAll(IDBKeyRange.only(galleryId));
    videos.forEach((media) => {
      Gallery.addVideo(media);
    });
    tx.done;

    tx = db.transaction(MediaStorage.imageStore, 'readonly');
    store = tx.objectStore(MediaStorage.imageStore);
    index = store.index('galleryId');
    let images = await index.getAll(IDBKeyRange.only(galleryId));
    images.forEach((media) => {
      Gallery.addImage(media);
    });
    tx.done;
  }
}
