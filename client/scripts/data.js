const video_icon = L.divIcon({
    html: '<i class="fas fa-video"></i>',
    iconSize: [20, 20],
    className: 'media_icon'
});

var ws = new WebSocket("ws://" + REST_IP + ":" + REST_PORT + "/ws");
ws.onopen = function() {
   console.log('Open socket')
};
ws.onmessage = function (evt) {
    let data = JSON.parse(evt.data)
    console.log(data)
    let container = document.getElementById('conatiner')

    data['videos'].forEach(video => {
        let marker = L.marker([video.lat, video.lon], {
            icon: L.icon.glyph({
                prefix: 'fas',
                glyph: 'video'
            })
        })
        let popup = L.popup({maxWidth: '100%'});        
        let iframe = document.createElement('iframe');
            iframe.src=video.url;
            iframe.width=800;
            iframe.height=600;
        popup.setContent(iframe);
        marker.bindPopup(popup)
        marker.addTo(map);
    });

    data['images'].forEach(image => {
        let marker = L.marker([image.lat, image.lon], {
            icon: L.icon.glyph({
                prefix: 'fas',
                glyph: 'camera'
            })
        })
        let popup = L.popup({maxWidth: '100%'});   
        let map_image  = document.createElement('img')
        map_image.src = image.url;
        let iframe = document.createElement('iframe');
            iframe.width=800;
            iframe.height=600;
        let html = '<body>' +
                    '<img src="' + image.url + '"' + 'height="97%" width="100%">' +
                    '</body>';
        iframe.src = 'data:text/html;charset=utf-8,' + encodeURI(html);
        popup.setContent(iframe);
        marker.bindPopup(popup)
        marker.addTo(map);
    });
    ws.close()
};
