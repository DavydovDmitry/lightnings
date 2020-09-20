import {idFromLonLat} from "../locationId";
import {openDB} from "idb";
import {dbName, dbVersion, imageStore, videoStore} from "./config";

async function addMedia(objectStore, media) {
  const db = await openDB(dbName, dbVersion);
  const tx = db.transaction(objectStore, 'readwrite');
  const store = tx.objectStore(objectStore);
  if (await store.get(media.url) === undefined){
    await store.add({
      url: media.url,
      shortcode: media.shortcode,
      galleryId: idFromLonLat(media.lon, media.lat)
    });
  }
}

export async function addVideo(video) {
  await addMedia(videoStore, video);
}

export async function addImage(image) {
  await addMedia(imageStore, image)
}
