import requests
import pandas as pd


class ESPNRequester:
    def __init__(self, league_id: int, season_id: int, swid: str = None, espn_s2: str = None):
        self.league_id = league_id
        self.season_id = season_id
        self.url = f"https://fantasy.espn.com/apis/v3/games/flb/seasons/{season_id}/segments/0/leagues/{league_id}"
        self.cookies = dict(swid=swid, espn_s2=espn_s2)

    def get_teams(self):
        """
        Returns JSON data for each team in the league
        :return: dict
        """
        params = {"view": "mTeam"}
        r = requests.get(self.url, params=params, cookies=self.cookies)
        return r.json()["teams"]

    def get_daily_stats(self, scoring_period_id: int):
        """
        Grabs the roster and scoring information for the specified scoring period for all teams in the league
        :param scoring_period_id: The scoring period from which to grab stats from.
        :return: list
        """
        params = {"scoringPeriodId": f"{scoring_period_id}", "view": "mRoster"}
        r = requests.get(self.url, params=params, cookies=self.cookies)
        return r.json()["teams"]

    def get_team_daily_stats(self, team_id, scoring_period_id):
        params = {"forTeamId": f"{team_id}", "scoringPeriodId": f"{scoring_period_id}", "view": "mRoster"}
        cookies = self.cookies
        r = requests.get(self.url, params=params, cookies=cookies)
        json = r.json()
        df_columns = ["team_id", "player_id", "scoring_period_id", "lineup_id"]
        df = pd.DataFrame(columns=df_columns)
        players = json["teams"][0]["roster"]["entries"]
        for player in players:
            d = {"team_id": team_id, "player_id": player["playerId"], "scoring_period_id": scoring_period_id,
                 "lineup_id": player["lineupSlotId"]}
            for stat_set in player["playerPoolEntry"]["player"]["stats"]:
                if stat_set["statSourceId"] == 0 and stat_set["statSplitTypeId"] == 5:
                    d.update(stat_set["stats"])
            df = df.append(d, ignore_index=True)
        return df

    @staticmethod
    def commit_to_db(df, table, db):
        df.to_sql(table, db)