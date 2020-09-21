# Lightnings
This project build a map (using [OpenLayers](https://openlayers.org/en/latest/apidoc/)) of thunderstorms with multimedia (images and videos) from Instagram.
<p>
<img align="right" width="200" src="/client/src/images/logo.ico">

Essential processing stages:
- collect locations and time of thinderstorms from [Thunderfinder](http://lightnings.ru/);
- collect multimedia from [Instagram](https://www.instagram.com/explore/tags/%D0%BC%D0%BE%D0%BB%D0%BD%D0%B8%D1%8F/):
    - collect shortcodes of multimedia by tag;
    - collect time and location of multimedia;
- display on map icons of lightnings (on click multimedia) if time and location from **Instagram** and from **Thunderfinder** are **the same**.  
</p>

## Run
```shell script
docker-compose build &&
docker-compose up
```
