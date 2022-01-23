import requests
import yaml
from .entities import Match, Team, MatchStats, Venue
from .exceptions import ValueNotFound, BadResponse


class SportDataApi:
    def __init__(self):
        self.api_key = self.__get_api_key()

    def get_response(self, endpoint, params={}):
        headers = {"apikey": self.api_key}

        res = requests.get(
            f"https://app.sportdataapi.com/api/v1/soccer/{endpoint}",
            headers=headers,
            params=params,
        )
        if res.status_code == 200:
            return res.json()["data"]

        else:
            raise BadResponse

    def get_matches(self, country, league, season, date_from):
        try:
            season_id = self.__get_season_id(country, league, season)
            params = {"season_id": season_id, "date_from": date_from}
            res = self.get_response("matches", params=params)
        except ValueNotFound:
            print("Season ID not found")
            return None
        except BadResponse:
            print("Bad response from SportData")
            return None

        matches = []
        for mtch in res:
            match_id = mtch["match_id"]
            status = mtch["status"]
            match_start_iso = mtch["match_start_iso"]
            minute = mtch["minute"]
            referee_id = mtch["referee_id"]
            h_team = mtch["home_team"]
            a_team = mtch["away_team"]
            stats = mtch["stats"]
            ven = mtch["venue"]

            home_team = Team(
                h_team["team_id"], h_team["name"], h_team["short_code"], h_team["logo"]
            )
            away_team = Team(
                a_team["team_id"], a_team["name"], a_team["short_code"], a_team["logo"]
            )

            match_stats = MatchStats(
                stats["home_score"],
                stats["away_score"],
                stats["ht_score"],
                stats["ft_score"],
                stats["et_score"],
                stats["ps_score"],
            )

            if ven:
                venue = Venue(
                    ven["venue_id"],
                    ven["name"],
                    ven["capacity"],
                    ven["city"],
                    ven["country_id"],
                )
            else:
                venue = None

            matches.append(
                Match(
                    match_id,
                    status,
                    match_start_iso,
                    minute,
                    referee_id,
                    home_team,
                    away_team,
                    match_stats,
                    venue,
                )
            )
        return matches

    def __get_api_key(self):
        with open("keys.yml") as f:
            return yaml.safe_load(f)["sportdata_api_key"]

    def __get_league_id(self, country_id, league_name):
        params = {"country_id": country_id}
        res = self.get_response("leagues", params)

        if res:
            for key, league in res.items():
                if league["name"] == league_name:
                    return league["league_id"]
        else:
            raise ValueNotFound

    def __get_country_id(self, country):
        res = self.get_response("countries")
        if res:
            for idx, cntry in enumerate(res):
                if cntry["name"] == country:
                    return res[idx]["country_id"]
        else:
            raise ValueNotFound

    def __get_season_id(self, country, league_name, season):
        country_id = self.__get_country_id(country)
        league_id = self.__get_league_id(country_id, league_name)
        params = {"league_id": league_id}
        res = self.get_response("seasons", params)

        if res:
            for idx, sns in enumerate(res):
                if sns["name"] == season:
                    return res[idx]["season_id"]
        else:
            raise ValueNotFound
