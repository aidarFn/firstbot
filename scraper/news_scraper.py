import requests
from parsel import Selector


class NewsScraper:
    URL = 'https://animag.ru/news'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    }

    IMAGE_XPATH = '//img[@class="img-responsive"]/@src'
    TITLE_XPATH = '//h1[@class="page-header"]/text()'
    LINK_XPATH = '//span[@class="field-content"]/a/@href'

    def scrape_data(self):
        response = requests.get(self.URL, headers=self.HEADERS)
        # print(response.text)
        tree = Selector(text=response.text)
        imgs = tree.xpath(self.IMAGE_XPATH).getall()
        titles = tree.xpath(self.TITLE_XPATH).getall()
        links = tree.xpath(self.LINK_XPATH).getall()
        return links[:5]


if __name__ == '__main__':
    scraper = NewsScraper()
    scraper.scrape_data()