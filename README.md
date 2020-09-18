# Lightnings
This project build a map (using [OpenLayers](https://openlayers.org/en/latest/apidoc/)) of thunderstorms with multimedia (images and videos) from Instagram.

Essential processing stages:
- collect locations and time of thinderstorms from [Thunderfinder](http://lightnings.ru/);
- collect multimedia from [Instagram](https://www.instagram.com/explore/tags/%D0%BC%D0%BE%D0%BB%D0%BD%D0%B8%D1%8F/):
    - collect shortcodes of multimedia by tag;
    - collect time and location of multimedia;
- display on map icons of lightnings (on click multimedia) if time and location from **Instagram** and from **Thunderfinder** are **the same**.  

## Setup

- [Python](https://www.python.org/downloads/) >= 3.7
- [Poetry](https://python-poetry.org/docs/) >= 0.12

## Execution
```shell script
export $(cat .env) &&
docker-compose up
```
