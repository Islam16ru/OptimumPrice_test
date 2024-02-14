import json

import scrapy

from scrapy import Request, FormRequest

from TestTask.cheker import is_jsong

from TestTask.items import FilmItem

class FilmSpiderSpider(scrapy.Spider):
    name = "film_spider"
    allowed_domains = ["scrapethissite.com"]
    start_urls = ["https://scrapethissite.com/pages/ajax-javascript"]

    def parse(self, response):
        # проверка наличие в ответе с сервера данных в формате json
        data = is_jsong(response.body)

        if data:
            #Инициализация выходных данных и извлечения данных json
            film_item = FilmItem()

            #Выборка из ответа нужных частей данных
            for item in data:
                film_item['title'] = item.get('title')
                film_item['nominations'] = item.get('nominations')
                film_item['awards'] = item.get('awards')

                if item.get('best_picture'):
                    film_item['best_picture'] = 1
                else:
                    film_item['best_picture'] = 0

                yield film_item

        else:
            #Получения ссылок на json данные
            corrent_year = response.\
                xpath("//div[@class='col-md-12 text-center']/a[@class='year-link']/text()").getall()

            #Отправление запросов на получение данных
            for year in corrent_year:
                url_first_page = self.start_urls[0] + "/?ajax=true&year=" + year
                yield Request(url_first_page, callback=self.parse)


