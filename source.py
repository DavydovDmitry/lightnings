from lightnings_data.upload_lightnings import upload_lightnings
from instagram.scraper import Scraper


if __name__ == "__main__":
    #upload_lightnings()

    scraper = Scraper(tag='lightnings')
    print(len(scraper.get_urls(quantity=300)))