import requests
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)


class Summoner:
    def __init__(self, name, account_id, api_key):
        self.name = name
        self.account_id = account_id
        self.api_key = api_key

    def get_last_match_id(self):
        logger.info("Get match list for " + self.name)
        url = (
            f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.account_id}/ids"
            + "?api_key="
            + str(self.api_key)
        )
        r = requests.get(url)
        r_json = r.json()
        print(r_json)
        last_match = r_json["matches"][0]["gameId"]
        logger.info("Returning gameId of last match")
        return last_match
