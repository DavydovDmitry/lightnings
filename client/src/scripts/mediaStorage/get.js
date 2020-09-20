import {openDB} from "idb";
import {dbName, dbVersion, imageStore, videoStore} from "./config";

async function getMediaByGalleryId(objectStore, galleryId){
  const db = await openDB(dbName, dbVersion);
  const tx = db.transaction(objectStore, 'readonly');
  let store = tx.objectStore(objectStore);
  let index = store.index('galleryId');
  let media = await index.getAll(IDBKeyRange.only(galleryId));
  tx.done;
  return media;
}

export async function getImagesByGalleryId(galleryId) {
  return getMediaByGalleryId(imageStore, galleryId);
}

export async function getVideosByGalleryId(galleryId) {
  return getMediaByGalleryId(videoStore, galleryId);
}
