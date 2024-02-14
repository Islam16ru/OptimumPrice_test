import os

os.system('cmd /c "scrapy crawl film_spider -o date_film.json  & scrapy crawl hockey_teams_spider -o date_hockey.json "')