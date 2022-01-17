import pandas as pd
from espn_constant import HITTING_MAP, PITCHING_MAP, POSITION_MAP


class Team:
    def __init__(self, league_id: int, season_id: int, team_id: int, team_json: dict = None):
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
        self.hitting_columns = list()
        self.pitching_columns = list()
        self.create_frames()
        if self.team_json is not None:
            self.update_team_info(self.team_json)
            self.update_season_stats(self.team_json)

    def __repr__(self):
        return f"team: {self.team_id}"

    def create_frames(self):
        """
        Creates a list of the pitching and hitting columns to be used in the statistical DataFrames.
        The column lists are stored in the Team attributes.
        :return: None
        """
        for stat in HITTING_MAP:
            self.hitting_columns.append(stat)
        for stat in PITCHING_MAP:
            self.pitching_columns.append(stat)

    def update_team_info(self, team_json: dict):
        """
        Updates the information for each team in the league.
        :param team_json: JSON data for the team
        :return: None
        """
        data = team_json
        self.abbrev = data["abbrev"]
        self.division_id = data["divisionId"]
        self.location = data["location"]
        self.logo = data["logo"]
        self.nickname = data["nickname"]
        self.swid = data["primaryOwner"]
        self.record = data["record"]["overall"]
        self.transaction_counter = data["transactionCounter"]

    def update_season_stats(self, team_json):
        """
        Parses the JSON data for the team and stores the total hitting and pitching stats for the team in attributes.
        :param team_json: JSON data for the team
        :return: None
        """
        data = team_json["valuesByStat"]
        hitting_dict = {}
        pitching_dict = {}
        for stat in data:
            stat = int(stat)
            if stat <= 31:
                hitting_dict[HITTING_MAP[stat]] = data[str(stat)]
            elif 33 <= stat <= 66:
                pitching_dict[PITCHING_MAP[stat]] = data[str(stat)]
        self.season_hitting = pd.DataFrame(hitting_dict, index={self.team_id})
        self.season_hitting.index.name = 'team_id'
        self.season_pitching = pd.DataFrame(pitching_dict, index={self.team_id})
        self.season_pitching.index.name = 'team_id'

    def get_daily_stats(self, roster_json: dict):
        """
        Parses the JSON info returned from the ESPN API and stores the statistics of the team in a DataFrame.
        Need to sort stats for ease of viewing.
        :param roster_json: The team roster JSON returned from the ESPN API for the specified scoring period.
        :return: Pandas DataFrame
        """
        df_columns = ["team_id", "player_id", "scoring_period_id", "lineup_id", "position"]
        df = pd.DataFrame(columns=df_columns)
        for player in roster_json:
            player_dict = {"team_id": self.team_id, "player_id": player["playerId"],
                           "lineup_id": player["lineupSlotId"], "position": POSITION_MAP[player["lineupSlotId"]]}
            for stat_set in player["playerPoolEntry"]["player"]["stats"]:
                if stat_set["statSourceId"] == 0 and stat_set["statSplitTypeId"] == 5:
                    player_dict["scoring_period_id"] = stat_set["scoringPeriodId"]
                    # checks if the player is in an active hitting spot and adds hitting stats to the player dict
                    if int(player_dict["lineup_id"]) <= 12 or int(player_dict["lineup_id"]) == 19:
                        player_dict.update(self.process_hitting_stats(stat_set["stats"]))
                    # checks if the player is in an active pitching spot and adds pitching stats to the player dict
                    elif 13 <= int(player_dict["lineup_id"]) <= 15:
                        player_dict.update(self.process_pitching_stats(stat_set["stats"]))
            df = df.append(player_dict, ignore_index=True)
        return df

    @staticmethod
    def process_hitting_stats(stat_dict):
        """
        Takes a stat dictionary found in the roster JSON data and returns a dictionary with the hitting statistic names as
        keys and their respective values as values.
        :param stat_dict: statistic dictionary taken from roster JSON data
        :return: human readable hitting dictionary
        """
        hitting_columns = []
        for stat in HITTING_MAP:
            hitting_columns.append(HITTING_MAP[stat])
        hitting_dict = dict()
        for stat in stat_dict:
            stat = int(stat)
            if stat <= 31:
                hitting_dict[HITTING_MAP[stat]] = stat_dict[str(stat)]
        return hitting_dict

    @staticmethod
    def process_pitching_stats(stat_dict):
        pitching_dict = dict()
        for stat in stat_dict:
            stat = int(stat)
            if 33 <= stat <= 66:
                pitching_dict[PITCHING_MAP[stat]] = stat_dict[str(stat)]
        return pitching_dict

    def get_current_roster(self):
        pass
