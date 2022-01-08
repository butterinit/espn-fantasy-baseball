import pandas as pd
from espn_constant import STATS_MAP


class Team:
    def __init__(self, league_id, season_id, team_id, team_json=None):
        self.league_id = league_id
        self.season_id = season_id
        self.team_id = team_id
        self.current_roster = None
        self.season_hitting = None
        self.season_pitching = None
        self.record = None
        self.logo = None
        self.swid = None
        self.abbrev = None
        self.location = None
        self.nickname = None
        self.transaction_counter = None
        self.division_id = None
        self.team_json = team_json
        if self.team_json is not None:
            self.get_info(self.team_json)
            self.get_season_stats(self.team_json)

    def __str__(self):
        return f"team: {self.team_id}"

    def get_info(self, team_json):
        data = team_json
        self.abbrev = data["abbrev"]
        self.division_id = data["divisionId"]
        self.location = data["location"]
        self.logo = data["logo"]
        self.nickname = data["nickname"]
        self.swid = data["primaryOwner"]
        self.record = data["record"]["overall"]
        self.transaction_counter = data["transactionCounter"]

    def get_season_stats(self, team_json):
        data = team_json["valuesByStat"]
        hitting_dict = {}
        pitching_dict = {}
        for stat in data:
            stat = int(stat)
            if stat <= 31:
                hitting_dict[STATS_MAP[stat]] = data[str(stat)]
            elif 33 <= stat <= 66:
                pitching_dict[STATS_MAP[stat]] = data[str(stat)]
        self.season_hitting = pd.DataFrame(hitting_dict, index={self.team_id})
        self.season_hitting.index.name = 'team_id'
        self.season_pitching = pd.DataFrame(pitching_dict, index={self.team_id})
        self.season_pitching.index.name = 'team_id'

    def get_daily_stats(self, roster_json):
        # need to sort stats by pitching or hitting
        df_columns = ["team_id", "player_id", "scoring_period_id", "lineup_id"]
        df = pd.DataFrame(columns=df_columns)
        for player in roster_json:
            d = {"team_id": self.team_id, "player_id": player["playerId"], "scoring"
                 "lineup_id": player["lineupSlotId"]}
            for stat_set in player["playerPoolEntry"]["player"]["stats"]:
                if stat_set["statSourceId"] == 0 and stat_set["statSplitTypeId"] == 5:
                    d["scoring_period_id"] = stat_set["scoringPeriodId"]
                    d.update(stat_set["stats"])
            df = df.append(d, ignore_index=True)
        return df

    def get_current_roster(self):
        pass
