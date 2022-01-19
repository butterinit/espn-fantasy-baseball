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
        self.final_scoring_period = None
        self.get_league_info()
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
        hitting_df = pd.DataFrame()
        pitching_df = pd.DataFrame()
        for team in self.teams:
            team_roster_json = league_roster_json[team.team_id-1]["roster"]["entries"]
            hitting, pitching = team.get_daily_stats(team_roster_json)
            hitting_df = hitting_df.append(hitting)
            pitching_df = pitching_df.append(pitching)
        return hitting_df, pitching_df

    def get_all_daily_stats(self, hitting_file: str = "total daily hitting.xlsx", pitching_file:
                            str = "total daily pitching.xlsx"):
        """
        gets daily stats for the entire season and outputs the data as two seperate excel files.
        todo: combine the files into one workbook
        :param hitting_file:
        :param pitching_file:
        :return: None
        """
        hitting_df = pd.DataFrame()
        pitching_df = pd.DataFrame()
        for i in range(1, self.final_scoring_period+1):
            hitting, pitching = self.update_daily_statistics(i)
            hitting_df = hitting_df.append(hitting)
            pitching_df = pitching_df.append(pitching)
        hitting_df.to_excel(hitting_file)
        pitching_df.to_excel(pitching_file)

    def get_league_info(self):
        """
        gathers league settings and stores them in attributes
        todo: add roster settings and scoring settings
        :return: None
        """
        settings_json = self.req.get_league_settings()
        self.final_scoring_period = int(settings_json["status"]["finalScoringPeriod"])
