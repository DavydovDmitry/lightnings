# Lightnings
This project build map of lighnings and display it's multimedia (images and video) from Instagram.

Essential stages:
- collect locations and time of thinderstorms from thunderfinder site;
- collect multimedia from Instagram
    - collect shortcodes of multimedia by tag
    - collect time and precise location of multimedia
- display on map lightnings (on click multimedia) if time and location from Instagram and from thunderfinder are the same.  

### Execution
```shell script
export $(cat local.env) &&
docker-compose up
```
