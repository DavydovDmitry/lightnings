const xhr = new XMLHttpRequest();
xhr.open('GET', `http://${REST_IP}:${REST_PORT}/meteo`);
xhr.onload = async (evt) => {
  let data = JSON.parse(evt.target.response);
  await MediaStorage.createStores();

  data['videos'].forEach(video => {
      let marker = L.marker([video.lat, video.lng], {
          icon: L.icon.glyph({
              prefix: 'fas',
              glyph: 'video'
          })
      })
      MediaStorage.addVideo(video)
      marker.on('click', Gallery.show);
      marker.addTo(map);
  });

  data['images'].forEach(image => {
      let marker = L.marker([image.lat, image.lng], {
          icon: L.icon.glyph({
              prefix: 'fas',
              glyph: 'camera'
          })
      })
      MediaStorage.addImage(image);
      marker.on('click', Gallery.show);
      marker.addTo(map);
  });
};
xhr.send();
