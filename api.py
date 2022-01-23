import requests
import yaml


class SportDataApi:
    def __init__(self):
        self.api_key = self.__get_api_key()


    def get_response(self, endpoint, params={}):
        headers = { 
        "apikey": self.api_key}

        res = requests.get(
        f"https://app.sportdataapi.com/api/v1/soccer/{endpoint}",
            headers=headers, params=params)
        if res.status_code == 200:
            return res.json()["data"]

        else:
            print("Error:", res.status_code)
            return None

    def get_matches(self, country, league, season, date_from):
        season_id = self.__get_season_id(country, league, season)

        params = {
            "season_id": season_id,
            "date_from": date_from
        }

        res = self.get_response(
            "matches",
            params=params)

        return res


    def __get_api_key(self):
        with open('keys.yml') as f:
            return yaml.safe_load(f)["sportdata_api_key"]       


    def __get_league_id(self, country_id, league_name):
        res = self.get_response("leagues")
        
        if res:
            for idx, league in enumerate(res):
                if league["name"] == league_name and league["country_id"] == country_id:
                    return res[idx]["league_id"] 
        else: 
            print("League not found")
            return None


    def __get_country_id(self, country):
        res = self.get_response("countries")
        if res:
            for idx, cntry in enumerate(res):
                if cntry["name"] == country:
                    return res[idx]["country_id"]
        else:
            print("Country not found")
            return None


    def __get_season_id(self, country, league_name, season):
        country_id = self.__get_country_id(country)
        league_id = self.__get_league_id(country_id, league_name)
        
        params = {
            "league_id": league_id
        }

        res = self.get_response("seasons", params)

        if res:
            for idx, sns in enumerate(res):
                if sns["name"] == season:
                    return res[idx]["season_id"]
        else:
            print("Season not found")
            return None


api = SportDataApi()
print(api.get_matches("England", "Premier League", "21/22", "2022-01-21"))