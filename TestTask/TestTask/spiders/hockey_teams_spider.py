import re

import scrapy

from scrapy import FormRequest, Request

from TestTask.items import HockeyTeamsResultItem

from TestTask.textworker import textnormalization

class HockeyTeamsSpiderSpider(scrapy.Spider):
    name = "hockey_teams_spider"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/forms/"]

    def start_requests(self):
        #Формирование стартового запроса
        form_data = {'q': "New York"}
        #Парсинг по запросу
        for start_url in self.start_urls:
            yield FormRequest(
                url=start_url,
                method='GET',
                formdata=form_data,
                callback=self.parse)

    def parse(self, response):
        #Инициация структуры для хранения данных
        team_result = HockeyTeamsResultItem()

        #Получение всех строк
        results = response.xpath("//tr[@class='team']")

        #Дастаем из все данные из запроса и возврощаем их
        for result in results:
            team_result['team_name'] = textnormalization(result.xpath("./td[@class='name']/text()").get())
            team_result['year'] = textnormalization(result.xpath("./td[@class='year']/text()").get())
            team_result['wins'] = textnormalization(result.xpath("./td[@class='wins']/text()").get())
            team_result['losses'] = textnormalization(result.xpath("./td[@class='losses']/text()").get())
            team_result['ot_losses'] = textnormalization(result.xpath("./td[@class='ot-losses']/text()").get())
            team_result['win_percent'] = textnormalization(result.xpath("./td[@class='pct text-danger']/text()").get())
            team_result['goals_for'] = textnormalization(result.xpath("./td[@class='gf']/text()").get())
            team_result['goals_against'] = textnormalization(result.xpath("./td[@class='ga']/text()").get())
            team_result['diff'] = textnormalization(result.xpath("./td[@class='diff text-danger']/text()").get())

            yield team_result

        #Проверка последняя ли это страница
        next_button = response.xpath("//ul[@class='pagination']/li/a[@aria-label='Next']")

        if next_button:
            #Получение даннях формы
            search_number = re.search("page_num=\d+", response.url)
            search_question = re.search("q=.+", response.url)

            if search_number:
                page_number = int(str.split(search_number[0], '=')[1])
            else:
                page_number = 1

            if search_question[0]:
                formdate = {'page_num': str(page_number + 1), 'q': str.split(search_question[0], '=')[1].replace("+", " ")}
            else:
                formdate = {'page_num': str(page_number + 1)}

            #Переход на следующую страницу
            return FormRequest.from_response(response=response,
                                            formdata=formdate,
                                            callback=self.parse)