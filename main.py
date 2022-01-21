from League import League

if __name__ == '__main__':
    league_id = 123456789
    year = 2021
    # swid and espn_s2 are only needed for private leagues
    swid = "{XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}"
    espn_s2 = "long string................................................................................" \
              "%2goes....................................................................................." \
              "%2here..................................................................................... "
    my_league = League(league_id, year, swid=swid, espn_s2=espn_s2)
    my_league.season_hitting.to_excel("season_hitting.xlsx")
    my_league.season_pitching.to_excel("season_pitching.xlsx")
    my_league.get_all_daily_stats()
    print(my_league.teams)