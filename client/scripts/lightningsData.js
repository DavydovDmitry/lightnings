const video_icon = L.divIcon({
  html: '<i class="fas fa-video"></i>',
  iconSize: [20, 20],
  className: 'media_icon'
});

const ws = new WebSocket("ws://" + REST_IP + ":" + REST_PORT + "/meteo");
ws.onopen = function() {
 console.log('Open socket')
};
ws.onmessage = async (evt) => {
  let data = JSON.parse(evt.data)
  console.log(data)
  ws.close()

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
