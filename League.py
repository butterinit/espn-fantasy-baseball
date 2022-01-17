import pandas as pd
from api_requests import ESPNRequester
from Team import Team


class League:
    def __init__(self, league_id, season_id, swid=None, espn_s2=None):
        self.req = ESPNRequester(league_id, season_id, swid, espn_s2)
        self.league_id = league_id
        self.season_id = season_id
        self.teams = []
        self.season_hitting = pd.DataFrame()
        self.season_pitching = pd.DataFrame()
        self.last_scoring_period = None
        self.update_teams()
        self.update_season_statistics()

    def update_teams(self):
        """
        Initializes and adds a new Team object for each team in the league,
        and adds it to the teams attribute for the League.
        """
        data = self.req.get_teams()
        team_quantity = len(data)
        for team_id in range(1, team_quantity+1):
            team_data = data[team_id-1]
            new_team = Team(self.league_id, self.season_id, team_id, team_json=team_data)
            self.teams.append(new_team)

    def update_season_statistics(self):
        """
        Updates the season statistics DataFrames for the league.
        :return: None
        """
        for team in self.teams:
            self.season_hitting = self.season_hitting.append(team.season_hitting)
            self.season_pitching = self.season_pitching.append(team.season_pitching)

    def update_daily_statistics(self, scoring_period_id: int):
        """
        Gets statistics for the players on each roster in the league for the specified scoring period.
        :param scoring_period_id: The scoring period for which statistics will be gathered.
        :return: A DataFrame containing the league statistics for the scoring period.
        """
        league_roster_json = self.req.get_daily_stats(scoring_period_id=scoring_period_id)
        df = pd.DataFrame()
        for team in self.teams:
            team_roster_json = league_roster_json[team.team_id-1]["roster"]["entries"]
            new_row = team.get_daily_stats(team_roster_json)
            df = df.append(new_row)
        return df

    def get_league_info(self, commit: bool = False):
        # things to grab: final scoring period, team information, settings
        pass

    def populate_stats(self):
        # this should get the daily stats for the entire season for each team
        pass
