import asyncio
import httpx
from parsel import Selector


class AsyncNewsScrapper:
    URL = 'https://animag.ru/news'
    MAIN_URL = 'https://animag.ru/?page={page}'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    }

    IMAGE_XPATH = '//img[@class="img-responsive"]/@src'
    TITLE_XPATH = '//h1[@class="page-header"]/text()'
    LINK_XPATH = '//span[@class="field-content"]/a/@href'

    async def fetch_page(self, client, page):
        url = self.URL.format(page=page)
        response = await client.get(url, timeout=20.0)
        print("page:", page)
        # print(response.text)
        return Selector(response.text)

    async def scraper_data(self, selector):
        links = selector.xpath(self.LINK_XPATH).getall()
        print(links)

    async def get_pages(self, limit=20):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            get_page_tasks = [self.fetch_page(client, page) for page in range(1, limit + 1)]
            pages = await asyncio.gather(*get_page_tasks)

            scraping_tasks = [self.scraper_data(selector) for selector in pages if pages is not None]
            await asyncio.gather(*scraping_tasks)


if __name__ == '__main__':
    scraper = AsyncNewsScrapper()
    asyncio.run(scraper.get_pages())