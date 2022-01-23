import requests
import yaml


class SportDataApi:
    def __init__(self, country, league, season, date_from):
        self.country = country
        self.league = league
        self.season = season
        self.date_from = date_from
        self.api_key = self.get_api_key()


    def get_api_key(self):
        with open('keys.yml') as f:
            return yaml.safe_load(f)["sportdata_api_key"]       


    def get_response(self, endpoint, params={}):
        headers = { 
        "apikey": "7d6d2360-7bca-11ec-8a3a-c326f10ae11e"}

        res = requests.get(
        f"https://app.sportdataapi.com/api/v1/soccer/{endpoint}",
            headers=headers, params=params)
        if res.status_code == 200:
            return res.json()["data"]

        else:
            print("Error:", res.status_code)
            return None


    def get_league_id(self, country_id):
        res = self.get_response("leagues")
        
        if res:
            for idx, league in enumerate(res):
                if league["name"] == self.league and league["country_id"] == country_id:
                    return res[idx]["league_id"] 
        else: 
            print("League not found")
            return None


    def get_country_id(self):
        res = self.get_response("countries")
        if res:
            for idx, cntry in enumerate(res):
                if cntry["name"] == self.country:
                    return res[idx]["country_id"]
        else:
            print("Country not found")
            return None


    def get_season_id(self):
        country_id = self.get_country_id()
        league_id = self.get_league_id(country_id)
        
        params = {
            "league_id": league_id
        }

        res = self.get_response("seasons", params)

        if res:
            for idx, sns in enumerate(res):
                if sns["name"] == self.season:
                    return res[idx]["season_id"]
        else:
            print("Season not found")
            return None


    def get_matches(self):
        season_id = self.get_season_id()

        params = {
            "season_id": season_id,
            "date_from": self.date_from
        }

        res = self.get_response(
            "matches",
            params=params)

        return res


api = SportDataApi("England", "Premier League", "21/22", "2022-01-21")
print(api.get_matches())