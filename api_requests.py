import requests


class ESPNRequester:
    def __init__(self, league_id: int, season_id: int, swid: str = None, espn_s2: str = None):
        self.league_id = league_id
        self.season_id = season_id
        # The base url for api requests of the specified fantasy league.  Only valid for season_id > 2018
        if self.season_id >= 2018:
            self.url = f"https://fantasy.espn.com/apis/v3/games/flb/seasons/{season_id}/segments/0/leagues/{league_id}"
        elif self.season_id <= 2017:
            self.url = f"https://fantasy.espn.com/apis/v3/games/flb/leagueHistory/{league_id}?seasonId={season_id}"
        self.cookies = dict(swid=swid, espn_s2=espn_s2)

    def get_teams(self):
        """
        Returns JSON data for each team in the league
        :return: dict
        """
        params = {"view": "mTeam"}
        r = requests.get(self.url, params=params, cookies=self.cookies)
        print(r.url)
        if self.season_id < 2018:
            return r.json()[0]["teams"]
        else:
            return r.json()["teams"]

    def get_daily_stats(self, scoring_period_id: int):
        """
        Grabs the roster and scoring information for the specified scoring period for all teams in the league
        :param scoring_period_id: The scoring period from which to grab stats from.
        :return: list
        """
        params = {"scoringPeriodId": f"{scoring_period_id}", "view": "mRoster"}
        r = requests.get(self.url, params=params, cookies=self.cookies)
        print(r.url)
        if self.season_id < 2018:
            return r.json()[0]["teams"]
        else:
            return r.json()["teams"]

    def get_league_settings(self):
        """
        Grabs league settings and status
        :return: dictionary
        """
        params = {"view": "mSettings"}
        r = requests.get(self.url, params=params, cookies=self.cookies)
        print(r.url)
        if self.season_id < 2018:
            return r.json()[0]
        else:
            return r.json()
