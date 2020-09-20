import {openDB} from "idb";
import {dbName, dbVersion, imageStore, videoStore} from "./config";

async function putMedia(objectStore, shortcode, media) {
  const db = await openDB(dbName, dbVersion);
  const tx = db.transaction(objectStore, 'readwrite');
  const store = tx.objectStore(objectStore);
  await store.put(media, shortcode);
}

export async function putVideo(shortcode, video) {
  await putMedia(videoStore, shortcode, video);
}

export async function putImage (image, shortcode) {
  await putMedia(imageStore, shortcode, image);
}
