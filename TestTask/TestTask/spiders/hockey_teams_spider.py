import re

import scrapy

from scrapy import FormRequest, Request

from TestTask.items import HockeyTeamsResultItem

from TestTask.itemsloaders import HockeyTeamsResultItemLoader



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

        #Получение всех строк
        results = response.xpath("//tr[@class='team']")

        #Дастаем из все данные из запроса и возврощаем их
        for result in results:
            team_result = HockeyTeamsResultItemLoader(item=HockeyTeamsResultItem(), selector=result)
            team_result.add_xpath('team_name', "./td[@class='name']/text()")
            team_result.add_xpath('year', "./td[@class='year']/text()")
            team_result.add_xpath('wins', "./td[@class='wins']/text()")
            team_result.add_xpath('losses', "./td[@class='losses']/text()")
            team_result.add_xpath('ot_losses', "./td[@class='ot-losses']/text()")
            team_result.add_xpath('win_percent', "./td[@class='pct text-danger']/text() | ./td[@class='pct text-success']/text() ")
            team_result.add_xpath('goals_for', "./td[@class='gf']/text()")
            team_result.add_xpath('goals_against', "./td[@class='ga']/text()")
            team_result.add_xpath('diff', "./td[@class='diff text-danger']/text() | ./td[@class='diff text-success']/text() ")

            yield team_result.load_item()

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
            yield FormRequest.from_response(response=response,
                                            formdata=formdate,
                                            callback=self.parse)