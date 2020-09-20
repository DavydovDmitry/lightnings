import {openDB} from "idb";
import {dbName, dbVersion, imageStore, videoStore} from "./config";

export async function createObjectStores() {
  await openDB(dbName, dbVersion, {
    upgrade(db, oldVersion, newVersion){
      let store;

      if (oldVersion < 1){
        store = db.createObjectStore(videoStore, {
          keyPath: 'url'
        });
        store.createIndex('galleryId', 'galleryId', {unique: false});
        store.createIndex('shortcode', 'shortcode', {unique: true});

        store = db.createObjectStore(imageStore, {
          keyPath: 'url'
        });
        store.createIndex('galleryId', 'galleryId', {unique: false});
        store.createIndex('shortcode', 'shortcode', {unique: true});
      } else {
        console.log('Cancel to create object Stores. DB has latter version.');
      }
    }
  });
}
