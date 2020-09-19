import {openDB} from 'idb'
import {Gallery} from "./gallery";
import {idFromLonLat} from "./map";

export let MediaStorage = {
  dbName: 'lightnings',
  dbVersion: 1,
  blobStorage: 'blob',
  videoStore: 'video',
  imageStore: 'image',

  createStores: async () => {
    await openDB(MediaStorage.dbName, MediaStorage.dbVersion, {
      upgrade(db, oldVersion, newVersion){
        let store;

        if (oldVersion < 1){
          store = db.createObjectStore(MediaStorage.videoStore, {
            keyPath: 'url'
          });
          store.createIndex('galleryId', 'galleryId', {unique: false});
          store.createIndex('shortcode', 'shortcode', {unique: true});

          store = db.createObjectStore(MediaStorage.imageStore, {
            keyPath: 'url'
          });
          store.createIndex('galleryId', 'galleryId', {unique: false});
          store.createIndex('shortcode', 'shortcode', {unique: true});

          store = db.createObjectStore(MediaStorage.blobStorage, {keyPath: 'shortcode'});
        } else {
          console.log('Latter db version');
        }
      }
    });
  },
  addBlob: async (blob) => {
    const db = await openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction([MediaStorage.blobStorage], 'readwrite');
    await tx.objectStore(MediaStorage.blobStorage).put(blob);
  },
  getBlobURL: async (shortcode) => {
    const db = await openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction(MediaStorage.blobStorage, 'readonly');
    const store = tx.objectStore(MediaStorage.blobStorage);
    const blob = await store.get(IDBKeyRange.only(shortcode));
    return blob.blob;
  },
  addVideo: async (video) => {
    const galleryId = idFromLonLat(video.lon,video.lat);

    const db = await openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction(MediaStorage.videoStore, 'readwrite');
    const store = tx.objectStore(MediaStorage.videoStore);
    if (await store.get(video.url) === undefined){
      await store.add({
        url: video.url,
        shortcode: video.shortcode,
        galleryId: galleryId
      });
    }
  },
  putVideo: async (video, shortcode) => {
    const db = await openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction(MediaStorage.videoStore, 'readwrite');
    const store = tx.objectStore(MediaStorage.videoStore);
    await store.put(video, shortcode);
  },
  addImage: async (image) => {
    const galleryId = Gallery.idFromLocation({
        lat: image.lat,
        lng: image.lng
    });

    const db = await openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction(MediaStorage.imageStore, 'readwrite');
    const store = tx.objectStore(MediaStorage.imageStore);
    if (await store.get(image.url) === undefined){
      await store.add({
        url: image.url,
        shortcode: image.shortcode,
        galleryId: galleryId
      });
    }
  },
  putImage: async (image, shortcode) => {
    const db = await openDB(MediaStorage.dbName, MediaStorage.dbVersion);
    const tx = db.transaction(MediaStorage.imageStore, 'readwrite');
    const store = tx.objectStore(MediaStorage.imageStore);
    await store.put(image, shortcode);
  },
  toGallery: async (galleryId) => {
    const db = await openDB(MediaStorage.dbName, MediaStorage.dbVersion);

    let tx = db.transaction(MediaStorage.videoStore, 'readonly');
    let store = tx.objectStore(MediaStorage.videoStore);
    let index = store.index('galleryId');
    let videos = await index.getAll(IDBKeyRange.only(galleryId));
    tx.done;
    for (const video of videos){
      await updateVideo(video);
    }

    tx = db.transaction(MediaStorage.imageStore, 'readonly');
    store = tx.objectStore(MediaStorage.imageStore);
    index = store.index('galleryId');
    let images = await index.getAll(IDBKeyRange.only(galleryId));
    tx.done;
    images.forEach((media) => {
      Gallery.addImage(media);
    });
  }
}

export async function updateVideo(media) {
  const response = await fetch(media.url);
  if (!response.ok) {
    const extenction = media.url.split('?')[0].split('.').slice(-1)[0];
    const serverURL = `${REST_PROTOCOL}://${REST_IP}:${REST_PORT}/media/${media.shortcode + '.' + extenction}`;
    const xhr = new XMLHttpRequest();
    xhr.open('GET', serverURL);
    xhr.onload = async (evt) => {
      let blob = evt.target.response;

      await MediaStorage.addBlob({
        'blob': blob,
        'shortcode': media.shortcode
      });


      let video = Gallery.multimediaContainer.querySelector('video');
      const mediaBlob = await MediaStorage.getBlobURL(media.shortcode);
      let mediaSource = new MediaSource();
      video.src = URL.createObjectURL(mediaSource);
      mediaSource.addEventListener('sourceopen', () => {
        var mediaSource = this;
        var sourceBuffer = mediaSource.addSourceBuffer('video/mp4');
        sourceBuffer.addEventListener('updateend', function (_) {
          mediaSource.endOfStream();
          video.play();
        });
        sourceBuffer.appendBuffer(mediaBlob);
      });
    }
    xhr.send();
  } else {
    // Gallery.addVideo(media);
  }
}
