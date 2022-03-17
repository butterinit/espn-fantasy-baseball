<<<<<<< HEAD
import pandas as pd
from espn_constant import HITTING_MAP, PITCHING_MAP, POSITION_MAP, MATCHUP_PERIOD_MAP_2021


class Team:
    def __init__(self, team_json: dict = None):
        self.team_id = None
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
        self.hitting_frame = pd.DataFrame()
        self.pitching_frame = pd.DataFrame()
        self.create_frame_templates()
        if self.team_json is not None:
            self.update_team_info(self.team_json)
            self.update_season_stats(self.team_json)

    def __repr__(self):
        return f"{self.location} {self.nickname}"

    def create_frame_templates(self):
        """
        Creates a list of the pitching and hitting columns to be used in the statistical DataFrames.
        The column lists are stored in the Team attributes.
        :return: None
        """
        shared_columns = ["Team ID", "Player Name", "ESPN Player ID", "Scoring Period", "Matchup Period",
                          "Lineup ID", "Position"]
        hitting_columns = shared_columns.copy()
        pitching_columns = shared_columns.copy()
        for stat in HITTING_MAP:
            hitting_columns.append(HITTING_MAP[stat])
        for stat in PITCHING_MAP:
            pitching_columns.append(PITCHING_MAP[stat])
        self.hitting_frame = pd.DataFrame(columns=hitting_columns)
        self.pitching_frame = pd.DataFrame(columns=pitching_columns)

    def update_team_info(self, team_json: dict):
        """
        Updates the Team
        :param team_json: JSON data for the team
        :return: None
        """
        data = team_json
        self.team_id = data["id"]
        self.abbrev = data["abbrev"]
        self.division_id = data["divisionId"]
        self.location = data["location"]
        self.logo = data.get("logo")
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
        self.season_hitting.insert(0, "Team", self.location + self.nickname)
        self.season_pitching = pd.DataFrame(pitching_dict, index={self.team_id})
        self.season_pitching.index.name = 'team_id'
        self.season_pitching.insert(0, "Team", self.location + self.nickname)

    def get_daily_stats(self, roster_json: dict):
        """
        Parses the JSON info returned from the ESPN API and stores the statistics of the team in a DataFrame.
        Need to sort stats for ease of viewing.
        :param roster_json: The team roster JSON returned from the ESPN API for the specified scoring period.
        :return: Pandas DataFrame
        """
        hitting_df = self.hitting_frame.copy(deep=True)
        pitching_df = self.pitching_frame.copy(deep=True)
        for player in roster_json:
            player_dict = {"Team ID": self.team_id, "Player Name": player["playerPoolEntry"]["player"]["fullName"],
                           "ESPN Player ID": player["playerId"], "Lineup ID": player["lineupSlotId"],
                           "Position": POSITION_MAP[player["lineupSlotId"]]}
            for stat_set in player["playerPoolEntry"]["player"]["stats"]:
                if stat_set["statSourceId"] == 0 and stat_set["statSplitTypeId"] == 5:
                    player_dict["Scoring Period"] = stat_set["scoringPeriodId"]
                    for key in MATCHUP_PERIOD_MAP_2021:
                        if player_dict["Scoring Period"] in MATCHUP_PERIOD_MAP_2021[key]:
                            player_dict["Matchup Period"] = key
                    # checks if the player is in an active hitting spot and adds hitting stats to the player dict
                    if int(player_dict["Lineup ID"]) <= 12 or int(player_dict["Lineup ID"]) == 19:
                        player_dict.update(self.process_hitting_stats(stat_set["stats"]))
                        hitting_df = hitting_df.append(player_dict, ignore_index=True)
                    # checks if the player is in an active pitching spot and adds pitching stats to the player dict
                    elif 13 <= int(player_dict["Lineup ID"]) <= 15:
                        player_dict.update(self.process_pitching_stats(stat_set["stats"]))
                        pitching_df = pitching_df.append(player_dict, ignore_index=True)
        hitting_df.fillna(0, inplace=True)
        pitching_df.fillna(0, inplace=True)
        return hitting_df, pitching_df

    @staticmethod
    def process_hitting_stats(stat_dict):
        """
        Takes a stat dictionary found in the roster JSON data and returns a dictionary with the hitting statistic names
        as keys and their respective values as values.
        :param stat_dict: statistic dictionary taken from roster JSON data
        :return: human-readable hitting dictionary
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
        """
        Takes a stat dictionary found in the roster JSON data and returns a dictionary with the pitching statistic names
        as keys and their respective values as values.
        :param stat_dict: statistic dictionary taken from roster JSON data
        :return: human-readable pitching dictionary
        """
        pitching_dict = dict()
        for stat in stat_dict:
            stat = int(stat)
            if 33 <= stat <= 66:
                pitching_dict[PITCHING_MAP[stat]] = stat_dict[str(stat)]
        return pitching_dict

    def get_current_roster(self):
        pass
=======
import pandas as pd
from espn_constant import HITTING_MAP, PITCHING_MAP, POSITION_MAP, MATCHUP_PERIOD_MAP_2021


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
        self.hitting_frame = pd.DataFrame()
        self.pitching_frame = pd.DataFrame()
        self.create_frame_templates()
        if self.team_json is not None:
            self.update_team_info(self.team_json)
            self.update_season_stats(self.team_json)

    def __repr__(self):
        return f"{self.location} {self.nickname}"

    def create_frame_templates(self):
        """
        Creates a list of the pitching and hitting columns to be used in the statistical DataFrames.
        The column lists are stored in the Team attributes.
        :return: None
        """
        shared_columns = ["Team ID", "Player Name", "ESPN Player ID", "Scoring Period", "Matchup Period",
                          "Lineup ID", "Position"]
        hitting_columns = shared_columns.copy()
        pitching_columns = shared_columns.copy()
        for stat in HITTING_MAP:
            hitting_columns.append(HITTING_MAP[stat])
        for stat in PITCHING_MAP:
            pitching_columns.append(PITCHING_MAP[stat])
        self.hitting_frame = pd.DataFrame(columns=hitting_columns)
        self.pitching_frame = pd.DataFrame(columns=pitching_columns)

    def update_team_info(self, team_json: dict):
        """
        Updates the Team
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
        hitting_df = self.hitting_frame.copy(deep=True)
        pitching_df = self.pitching_frame.copy(deep=True)
        for player in roster_json:
            player_dict = {"Team ID": self.team_id, "Player Name": player["playerPoolEntry"]["player"]["fullName"],
                           "ESPN Player ID": player["playerId"], "Lineup ID": player["lineupSlotId"],
                           "Position": POSITION_MAP[player["lineupSlotId"]]}
            for stat_set in player["playerPoolEntry"]["player"]["stats"]:
                if stat_set["statSourceId"] == 0 and stat_set["statSplitTypeId"] == 5:
                    player_dict["Scoring Period"] = stat_set["scoringPeriodId"]
                    for key in MATCHUP_PERIOD_MAP_2021:
                        if player_dict["Scoring Period"] in MATCHUP_PERIOD_MAP_2021[key]:
                            player_dict["Matchup Period"] = key
                    # checks if the player is in an active hitting spot and adds hitting stats to the player dict
                    if int(player_dict["Lineup ID"]) <= 12 or int(player_dict["Lineup ID"]) == 19:
                        player_dict.update(self.process_hitting_stats(stat_set["stats"]))
                        hitting_df = hitting_df.append(player_dict, ignore_index=True)
                    # checks if the player is in an active pitching spot and adds pitching stats to the player dict
                    elif 13 <= int(player_dict["Lineup ID"]) <= 15:
                        player_dict.update(self.process_pitching_stats(stat_set["stats"]))
                        pitching_df = pitching_df.append(player_dict, ignore_index=True)
        return hitting_df, pitching_df

    @staticmethod
    def process_hitting_stats(stat_dict):
        """
        Takes a stat dictionary found in the roster JSON data and returns a dictionary with the hitting statistic names
        as keys and their respective values as values.
        :param stat_dict: statistic dictionary taken from roster JSON data
        :return: human-readable hitting dictionary
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
        """
        Takes a stat dictionary found in the roster JSON data and returns a dictionary with the pitching statistic names
        as keys and their respective values as values.
        :param stat_dict: statistic dictionary taken from roster JSON data
        :return: human-readable pitching dictionary
        """
        pitching_dict = dict()
        for stat in stat_dict:
            stat = int(stat)
            if 33 <= stat <= 66:
                pitching_dict[PITCHING_MAP[stat]] = stat_dict[str(stat)]
        return pitching_dict

    def get_current_roster(self):
        pass
>>>>>>> acb2ee0d95f3e9484687e39e7082d13e1871271c
