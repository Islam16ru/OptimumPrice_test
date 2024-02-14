# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmItem(scrapy.Item):
    title = scrapy.Field()
    nominations = scrapy.Field()
    awards = scrapy.Field()
    best_picture = scrapy.Field()

class HockeyTeamsResultItem(scrapy.Item):
    team_name = scrapy.Field()
    year = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    ot_losses = scrapy.Field()
    win_percent = scrapy.Field()
    goals_for= scrapy.Field()
    goals_against = scrapy.Field()
    diff = scrapy.Field()


