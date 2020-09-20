import {createObjectStores} from "./create"
import {addImage, addVideo} from "./add";
import {getImagesByGalleryId, getVideosByGalleryId} from "./get";
import {putImage, putVideo} from "./put";

export const MediaStorage = {
  createObjectStores: createObjectStores,

  addImage: addImage,
  addVideo: addVideo,

  getImagesByGalleryId: getImagesByGalleryId,
  getVideosByGalleryId: getVideosByGalleryId,

  putImage: putImage,
  putVideo: putVideo
}
