import re

from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class HockeyTeamsResultItemLoader(ItemLoader):

    def textnormalization(text):
        pattern = "^\s+|\n|\r|\s+$"

        outtext = ""

        if text:
            outtext = re.sub(pattern, '', text)

        return outtext

    default_output_processor = TakeFirst()
    team_name_in = MapCompose(textnormalization)
    year_in = MapCompose(textnormalization)
    wins_in = MapCompose(textnormalization)
    losses_in = MapCompose(textnormalization)
    ot_losses_in = MapCompose(textnormalization)
    win_percent_in = MapCompose(textnormalization)
    goals_for_in = MapCompose(textnormalization)
    goals_against_in = MapCompose(textnormalization)
    diff_in = MapCompose(textnormalization)
