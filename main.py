from League import League

if __name__ == '__main__':
    # your league_id can be found in the url of one of your league web pages
    league_id = 123456789
    year = 2021

    # swid and espn_s2 are only needed for private leagues
    swid = "{XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}"
    espn_s2 = "long string................................................................................" \
              "%2goes....................................................................................." \
              "%2here..................................................................................... "

    # Create a league object
    my_league = League(league_id, year, swid=swid, espn_s2=espn_s2)

    # season_hitting and season_pitching are dataframes containing the total stats accumulated for each team
    my_league.season_hitting.to_excel("season_hitting.xlsx")
    my_league.season_pitching.to_excel("season_pitching.xlsx")

    # The get_all_daily_stats method gets the stat line for each player in a team's active roster spot for the season
    # By default these will be stored in excel workbooks in the same folder as this file
    my_league.get_all_daily_stats()

    # Prints a list of each team in the league
    print(my_league.teams)

    # Stores the first team in the list of teams in a variable to simplify the syntax for the next step
    first_team = my_league.teams[0]

    # You can access information about each team by calling attributes
    # Examples of some of the information that is retrievable can be seen below
    print(first_team.logo)
    print(first_team.abbreviation)
    print(first_team.nickname)