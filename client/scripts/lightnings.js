const video_icon = L.divIcon({
    html: '<i class="fas fa-video"></i>',
    iconSize: [20, 20],
    className: 'media_icon'
});

const ws = new WebSocket("ws://" + REST_IP + ":" + REST_PORT + "/ws");
ws.onopen = function() {
   console.log('Open socket')
};
ws.onmessage = function (evt) {
    let data = JSON.parse(evt.data)
    console.log(data)

    data['videos'].forEach(video => {
        let marker = L.marker([video.lat, video.lng], {
            icon: L.icon.glyph({
                prefix: 'fas',
                glyph: 'video'
            })
        })
        let gallery = new Gallery(video);
        gallery.addVideo(video);
        marker.on('click', showGallery);
        marker.addTo(map);
    });

    data['images'].forEach(image => {
        let marker = L.marker([image.lat, image.lng], {
            icon: L.icon.glyph({
                prefix: 'fas',
                glyph: 'camera'
            })
        })
        let gallery = new Gallery(image);
        gallery.addImage(image);
        marker.on('click', showGallery);
        marker.addTo(map);
    });
    ws.close()
};
