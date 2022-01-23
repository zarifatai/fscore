class Match:
    def __init__(self, match_id, status, match_start_iso, minute, referee_id, home_team, away_team, stats, venue):
        self.match_id = match_id
        self.status = status
        self.match_start_iso = match_start_iso
        self.minute = minute
        self.referee_id = referee_id
        self.home_team = home_team
        self.away_team = away_team
        self.stats = stats
        self.venue = venue 


class Team:
    def __init__(self, team_id, name, short_code, logo):
        self.team_id = team_id
        self.name = name
        self.short_code = short_code
        self.logo = logo


class MatchStats:
    def __init__(self, home_score, away_score, ht_score, ft_score, et_score, ps_score):
        self.home_score = home_score
        self.away_score = away_score
        self.ht_score = ht_score
        self.ft_score = ft_score
        self.et_score = et_score
        self.ps_score = ps_score

class Venue:
    def __init__(self, venue_id, name, capacity, city, country_id):
        self.venue_id = venue_id
        self.name = name
        self.capacity = capacity
        self.city = city
        self.country_id = country_id
