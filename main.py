from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests

global_driver = webdriver.Chrome()

match_id = 0

base_url = 'https://www.vlr.gg/'

vct_apac_matches = 'https://www.vlr.gg/event/matches/2005/champions-tour-2024-pacific-stage-2/?series_id=3839'
vct_americas_matches = 'https://www.vlr.gg/event/matches/2095/champions-tour-2024-americas-stage-2/?series_id=4032'
vct_emea_matches = 'https://www.vlr.gg/event/matches/2094/champions-tour-2024-emea-stage-2/?series_id=4030'
vct_china_matches = 'https://www.vlr.gg/event/matches/2096/champions-tour-2024-china-stage-2/?series_id=4034'

vct_apac_matches_html = requests.get(vct_apac_matches)
vct_americas_matches_html = requests.get(vct_americas_matches)
vct_emea_matches_html = requests.get(vct_emea_matches)
vct_china_matches_html = requests.get(vct_china_matches)

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_matches_url(html_response):
    if html_response.status_code != 200:
        print('Error fetching page')
        return None
    
    matches_urls = []

    soup = BeautifulSoup(html_response.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        url = link.get('href')
        if url is None:
            continue
        url_parts = url.split('/')
        

        if len(url_parts) > 2 and isInt(url_parts[1]):
            combined_url = '/'.join([s for s in url_parts[1:]])
            match_url = base_url + combined_url
            matches_urls.append(match_url)
    
    return matches_urls

vct_apac_matches_urls = get_matches_url(vct_apac_matches_html)
vct_americas_matches_urls = get_matches_url(vct_americas_matches_html)
vct_emea_matches_urls = get_matches_url(vct_emea_matches_html)
vct_china_matches_urls = get_matches_url(vct_china_matches_html)

player_stats_columns = [
    "MatchID",
    "Map", 
    "Player", 
    "Team", 
    "Agent", 
    "Rating", 
    "Average Combat Score",
    "Kills",
    "Deaths",
    "Assists",
    "First Kills",
    "First Deaths",
]

match_columns = [
    "MatchID",
    "Winner",
    "Loser",
    "Winner Score",
    "Loser Score",
    "Picks and Bans",
]

df_vct_apac_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_apac_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)

df_vct_americas_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_americas_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)

df_vct_emea_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_emea_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)

df_vct_china_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_china_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)

def get_match_details(match_url):
    global match_id 
    match_id += 1

    global_driver.get(match_url)
    global_driver.implicitly_wait(0.5)
    
    match_entry = [match_id]

    match_header = global_driver.find_element(By.CLASS_NAME, 'match-header-vs')
    teams = match_header.find_elements(By.CLASS_NAME, 'wf-title-med')
    
    match_score_container = match_header.find_element(By.CLASS_NAME, 'match-header-vs-score')
    match_scores = match_score_container.find_element(By.CLASS_NAME, 'match-header-vs-score')

    #Get children of match_scores container - order of winner and loser score determines if left or right team won
    scores_container = match_scores.find_element(By.CLASS_NAME, 'js-spoiler')
    scores = scores_container.find_elements(By.XPATH, './*')

    winner = ''
    loser = ''

    for score in scores:
        if score.get_attribute('class') == 'match-header-vs-score-winner':
            winner = teams[0].text
            loser = teams[1].text
            break
        if score.get_attribute('class') == 'match-header-vs-score-loser':
            winner = teams[1].text
            loser = teams[0].text
            break


    winner_score = match_scores.find_element(By.CLASS_NAME, 'match-header-vs-score-winner').text
    loser_score = match_scores.find_element(By.CLASS_NAME, 'match-header-vs-score-loser').text
    picks_and_bans = global_driver.find_element(By.CLASS_NAME, 'match-header-note').text

    match_entry.append(winner)
    match_entry.append(loser)
    match_entry.append(winner_score)
    match_entry.append(loser_score)
    match_entry.append(picks_and_bans)

    return match_entry

    
# def get_player_stats(df_players_stats, match_id):
#     player_entry = [match_id]
#     stats_container = global_driver.find_element(By.CLASS_NAME, 'vm-stats')
#     maps = stats_container.find_elements(By.CLASS_NAME, 'vm-stats-gamesnav-item')
   

def get_player_stats_on_map(map, df_players_stats, match_id):
    #skip match overview and map if disabled (match already concluded)
    if 'mod-disabled' in map.get_attribute('class') or 'all' in map.get_attribute('data-game-id'):
        return df_players_stats
    
    map.click()
    global_driver.implicitly_wait(0.5)
    
    html_content = global_driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    map_name = soup.find('div', class_='vm-stats-gamesnav-item js-map-switch mod-active').text.strip()
    map_name_cleaned = map_name.split('\n')[2].replace('\t','')
    print(f"Map: {map_name_cleaned}")
    map_stats = soup.find('div', attrs={'class':'vm-stats-game', 'style':'display: block;'})
    teams_stats_table = map_stats.find_all('table', class_='wf-table-inset mod-overview')
    
    
    for team_stats_table in teams_stats_table:
        
        for i, row in enumerate(team_stats_table.find_all('tr')):
            if i == 0:
                continue #skip header row
            else:
                fields = row.find_all('td')
                new_row = [match_id, map_name_cleaned]
                skip_fields = [7, 8, 9, 10, 13]
                for idx, field in enumerate(fields):
                    if idx in skip_fields:
                        continue

                    field_class = field['class']

                    if 'mod-player' in field_class:
                        player_name = field.find('div', class_='text-of').text.strip()
                        new_row.append(player_name)
                        player_team = field.find('div', class_='ge-text-light').text.strip()
                        new_row.append(player_team)

                        print(f"Player {field.find('div', class_='text-of').text.strip()}")
                        print(f"Team {field.find('div', class_='ge-text-light').text.strip()}")
                    elif 'mod-agents' in field_class:
                        hero_played = field.find('img').get('alt')
                        new_row.append(hero_played)

                        print(f"Agent: {field.find('img').get('alt')}")
                    elif len(field_class) == 1 and (idx == 2 or idx == 3) and field_class[0] == 'mod-stat':
                        stat = field.find('span', class_='side mod-side mod-both') if field.find('span', class_='side mod-side mod-both') else field.find('span', class_='side mod-both')  
                        new_row.append(stat.text.strip())

                        print(f"{stat.text.strip()}")
                    elif 'mod-vlr-kills' in field_class:
                        num_kills = field.find('span', class_='side mod-side mod-both').text.strip()
                        new_row.append(num_kills)

                        print(f"Kills: {field.find('span', class_='side mod-side mod-both').text.strip()}")
                    elif 'mod-vlr-deaths' in field_class:
                        num_deaths = field.find('span', class_='side mod-both').text.strip()
                        new_row.append(num_deaths)

                        print(f"Deaths: {field.find('span', class_='side mod-both').text.strip()}")
                    elif 'mod-vlr-assists' in field_class:
                        num_assists = field.find('span', class_='side mod-both').text.strip()
                        new_row.append(num_assists)

                        print(f"Assists: {field.find('span', class_='side mod-both').text.strip()}")
                    elif 'mod-fb' in field_class:
                        num_fb = field.find('span', class_='side mod-both').text.strip()
                        new_row.append(num_fb)

                        print(f"First Kills: {field.find('span', class_='side mod-both').text.strip()}")
                    elif 'mod-fd' in field_class:
                        num_fk = field.find('span', class_='side mod-both').text.strip()
                        new_row.append(num_fk)

                        print(f"First Deaths: {field.find('span', class_='side mod-both').text.strip()}")

                print(new_row)
                df_players_stats.loc[len(df_players_stats)] = new_row
                new_row = []
    return df_players_stats

# def get_map_name(map_container):    
    # for map in maps_container_element:
    #     #mod-disabled class means match concluded before map was player; all is for match overview
    #     if 'mod-disabled' in map.get_attribute('class') or 'all' in map.get_attribute('data-game-id'):
    #         continue
        
    #     map.click()
    #     global_driver.implicitly_wait(0.5)
    #     html_content = global_driver.page_source

    #     soup = BeautifulSoup(html_content, 'html.parser')
        # map_name = soup.find('div', class_='vm-stats-gamesnav-item js-map-switch mod-active').text.strip()
        # map_name_cleaned = map_name.split('\n')[2].replace('\t','')

        # return map_name_cleaned

def get_player_and_match_stats(df_match_details, df_players_stats, matches_urls):
    
    for match_url in matches_urls:
        match_entry = get_match_details(match_url)
        df_match_details.loc[len(df_match_details)] = match_entry

        stats_container = global_driver.find_element(By.CLASS_NAME, 'vm-stats')
        maps = stats_container.find_elements(By.CLASS_NAME, 'vm-stats-gamesnav-item')
        
        for map in maps:
            df_players_stats = get_player_stats_on_map(map, df_players_stats, match_entry[0])

        

    return df_match_details, df_players_stats



df_vct_americas_season2_playoffs_match_details, df_vct_americas_season2_playoffs_player_stats = get_player_and_match_stats(df_vct_americas_season2_playoffs_match_details, 
                                                                                                                   df_vct_americas_season2_playoffs_player_stats, 
                                                                                                                   vct_americas_matches_urls)

df_vct_apac_season2_playoffs_match_details, df_vct_apac_season2_playoffs_player_stats = get_player_and_match_stats(df_vct_apac_season2_playoffs_match_details, 
                                                                                                                   df_vct_apac_season2_playoffs_player_stats,
                                                                                                                   vct_apac_matches_urls)

df_vct_emea_season2_playoffs_match_details, df_vct_emea_season2_playoffs_player_stats = get_player_and_match_stats(df_vct_emea_season2_playoffs_match_details,
                                                                                                                   df_vct_emea_season2_playoffs_player_stats,
                                                                                                                   vct_emea_matches_urls)

df_vct_china_season2_playoffs_match_details, df_vct_china_season2_playoffs_player_stats = get_player_and_match_stats(df_vct_china_season2_playoffs_match_details,
                                                                                                                     df_vct_china_season2_playoffs_player_stats,
                                                                                                                     vct_china_matches_urls)
    
df_vct_americas_season2_playoffs_match_details.to_csv('./csvs/vct_americas_season2_playoffs_match_details.csv', index=False)
df_vct_americas_season2_playoffs_player_stats.to_csv('./csvs/vct_americas_season2_playoffs_player_stats.csv', index=False)

df_vct_apac_season2_playoffs_match_details.to_csv('./csvs/vct_apac_season2_playoffs_match_details.csv', index=False)
df_vct_apac_season2_playoffs_player_stats.to_csv('./csvs/vct_apac_season2_playoffs_player_stats.csv', index=False)

df_vct_emea_season2_playoffs_match_details.to_csv('./csvs/vct_emea_season2_playoffs_match_details.csv', index=False)
df_vct_emea_season2_playoffs_player_stats.to_csv('./csvs/vct_emea_season2_playoffs_player_stats.csv', index=False)

df_vct_china_season2_playoffs_match_details.to_csv('./csvs/vct_china_season2_playoffs_match_details.csv', index=False)
df_vct_china_season2_playoffs_player_stats.to_csv('./csvs/vct_china_season2_playoffs_player_stats.csv', index=False)
    #player stats container
   

    # for map in maps:
        
    #     #skip match overview and map if disabled (match already concluded)
    #     if 'mod-disabled' in map.get_attribute('class') or 'all' in map.get_attribute('data-game-id'):
    #         continue
        
    #     map.click()
    #     global_driver.implicitly_wait(0.5)
        
    #     html_content = global_driver.page_source
    #     soup = BeautifulSoup(html_content, 'html.parser')
    #     map_name = soup.find('div', class_='vm-stats-gamesnav-item js-map-switch mod-active').text.strip()
    #     map_name_cleaned = map_name.split('\n')[2].replace('\t','')
    #     print(f"Map: {map_name_cleaned}")
    #     map_stats = soup.find('div', attrs={'class':'vm-stats-game', 'style':'display: block;'})
    #     teams_stats_table = map_stats.find_all('table', class_='wf-table-inset mod-overview')
       
       
    #     for team_stats_table in teams_stats_table:
            
    #         for i, row in enumerate(team_stats_table.find_all('tr')):
    #             if i == 0:
    #                 continue #skip header row
    #             else:
    #                 fields = row.find_all('td')
    #                 new_row = [match_id, map_name_cleaned]
    #                 skip_fields = [7, 8, 9, 10, 13]
    #                 for idx, field in enumerate(fields):
    #                     if idx in skip_fields:
    #                         continue

    #                     field_class = field['class']

    #                     if 'mod-player' in field_class:
    #                         player_name = field.find('div', class_='text-of').text.strip()
    #                         new_row.append(player_name)
    #                         player_team = field.find('div', class_='ge-text-light').text.strip()
    #                         new_row.append(player_team)

    #                         print(f"Player {field.find('div', class_='text-of').text.strip()}")
    #                         print(f"Team {field.find('div', class_='ge-text-light').text.strip()}")
    #                     elif 'mod-agents' in field_class:
    #                         hero_played = field.find('img').get('alt')
    #                         new_row.append(hero_played)

    #                         print(f"Agent: {field.find('img').get('alt')}")
    #                     elif len(field_class) == 1 and (idx == 2 or idx == 3) and field_class[0] == 'mod-stat':
    #                         stat = field.find('span', class_='side mod-side mod-both') if field.find('span', class_='side mod-side mod-both') else field.find('span', class_='side mod-both')  
    #                         new_row.append(stat.text.strip())

    #                         print(f"{stat.text.strip()}")
    #                     elif 'mod-vlr-kills' in field_class:
    #                         num_kills = field.find('span', class_='side mod-side mod-both').text.strip()
    #                         new_row.append(num_kills)

    #                         print(f"Kills: {field.find('span', class_='side mod-side mod-both').text.strip()}")
    #                     elif 'mod-vlr-deaths' in field_class:
    #                         num_deaths = field.find('span', class_='side mod-both').text.strip()
    #                         new_row.append(num_deaths)

    #                         print(f"Deaths: {field.find('span', class_='side mod-both').text.strip()}")
    #                     elif 'mod-vlr-assists' in field_class:
    #                         num_assists = field.find('span', class_='side mod-both').text.strip()
    #                         new_row.append(num_assists)

    #                         print(f"Assists: {field.find('span', class_='side mod-both').text.strip()}")
    #                     elif 'mod-fb' in field_class:
    #                         num_fb = field.find('span', class_='side mod-both').text.strip()
    #                         new_row.append(num_fb)

    #                         print(f"First Kills: {field.find('span', class_='side mod-both').text.strip()}")
    #                     elif 'mod-fd' in field_class:
    #                         num_fk = field.find('span', class_='side mod-both').text.strip()
    #                         new_row.append(num_fk)

    #                         print(f"First Deaths: {field.find('span', class_='side mod-both').text.strip()}")

    #                 print(new_row)
    #                 df_player_stats.loc[len(df_player_stats)] = new_row
    #                 new_row = []

global_driver.quit()

