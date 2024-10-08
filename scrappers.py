from bs4 import BeautifulSoup
from utils import isInt
from urls import base_url
from selenium.webdriver.common.by import By
from data import players_dict, maps_dict, teams_dict, agents_dict


match_id = 0


def get_matches_dates_and_urls(html_response):
    if html_response.status_code != 200:
        print('Error fetching page')
        return None
    
    matches_date_and_urls = []
    
    soup = BeautifulSoup(html_response.text, 'html.parser')
    
    wf_cards = soup.find_all('div', class_='wf-card')
    for wf_card in wf_cards:
        if wf_card.previous_sibling.previous_sibling is not None:
            date_raw = wf_card.previous_sibling.previous_sibling.text.strip()
            numerical_date = date_raw.split(',')[1:]
            date_string = ', '.join(s.strip() for s in numerical_date)
            

        links = wf_card.find_all('a')
        for link in links:
            url = link.get('href')
            if url is None:
                continue
            url_parts = url.split('/')
            

            if len(url_parts) > 2 and isInt(url_parts[1]):
                combined_url = '/'.join([s for s in url_parts[1:]])
                match_url = base_url + combined_url
                matches_date_and_urls.append((date_string, match_url))
                
    
    return matches_date_and_urls

def get_match_details(match_info_pair, selenium_driver):
    global match_id 
    match_id += 1

    selenium_driver.get(match_info_pair[1])
    selenium_driver.implicitly_wait(0.5)
    
    match_entry = [match_id, match_info_pair[0]]

    match_header = selenium_driver.find_element(By.CLASS_NAME, 'match-header-vs')
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
    picks_and_bans = selenium_driver.find_element(By.CLASS_NAME, 'match-header-note').text

    match_entry.append(winner)
    match_entry.append(loser)
    match_entry.append(winner_score)
    match_entry.append(loser_score)
    match_entry.append(picks_and_bans)

    return match_entry

def get_map_details(map_header):
    
    map_entry = [0, 0, "", "", ""]
    left_team_container = map_header.find('div', class_='team')
    right_team_container = map_header.find('div', class_='team mod-right')
    
    left_team_name = left_team_container.find('div', class_='team-name').text.strip()
    right_team_name = right_team_container.find('div', class_='team-name').text.strip()

    left_team_attack_score = int(left_team_container.find('span', class_='mod-t').text)
    left_team_defense_score = int(left_team_container.find('span', class_='mod-ct').text)
    left_team_ot_score = left_team_container.find('span', class_='mod-ot')
    left_team_total_score = left_team_attack_score + left_team_defense_score + int(left_team_ot_score.text) if left_team_ot_score else left_team_attack_score + left_team_defense_score

    right_team_attack_score = int(right_team_container.find('span', class_='mod-t').text)
    right_team_defense_score = int(right_team_container.find('span', class_='mod-ct').text)
    right_team_ot_score = right_team_container.find('span', class_='mod-ot')
    right_team_total_score = right_team_attack_score + right_team_defense_score + int(right_team_ot_score.text) if right_team_ot_score else right_team_attack_score + right_team_defense_score

    if left_team_total_score > right_team_total_score:
        map_entry[3] = left_team_name
        map_entry[4] = right_team_name
        map_entry.append(left_team_total_score)
        map_entry.append(left_team_attack_score)
        map_entry.append(left_team_defense_score)
        map_entry.append(right_team_total_score)
        map_entry.append(right_team_attack_score)
        map_entry.append(right_team_defense_score)
    else:
        map_entry[3] = right_team_name
        map_entry[4] = left_team_name
        map_entry.append(right_team_total_score)
        map_entry.append(right_team_attack_score)
        map_entry.append(right_team_defense_score)
        map_entry.append(left_team_total_score)
        map_entry.append(left_team_attack_score)
        map_entry.append(left_team_defense_score)
    
    return map_entry

def get_player_stats_on_map(selenium_driver, map, df_players_stats, df_map_details, match_id):
    #skip match overview and map if disabled (match already concluded)
    if 'mod-disabled' in map.get_attribute('class') or 'all' in map.get_attribute('data-game-id'):
        return df_players_stats
    
    map.click()
    selenium_driver.implicitly_wait(0.5)
    
    html_content = selenium_driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    map_name = soup.find('div', class_='vm-stats-gamesnav-item js-map-switch mod-active').text.strip()
    map_name_cleaned = map_name.split('\n')[2].replace('\t','')
    print(f"Map: {map_name_cleaned}")

    map_stats = soup.find('div', attrs={'class':'vm-stats-game', 'style':'display: block;'})

    map_header = map_stats.find('div', class_='vm-stats-game-header')
    map_entry = get_map_details(map_header)
    map_id = maps_dict[map_name_cleaned]
    map_entry[0] = match_id
    map_entry[1] = map_id
    map_entry[2] = map_name_cleaned
    df_map_details.loc[len(df_map_details)] = map_entry
    #map_entry = []
    

    
    teams_stats_table = map_stats.find_all('table', class_='wf-table-inset mod-overview')
    
    
    for team_stats_table in teams_stats_table:
        
        for i, row in enumerate(team_stats_table.find_all('tr')):
            if i == 0:
                continue #skip header row
            else:
                fields = row.find_all('td')
                new_row = [match_id, map_id, map_name_cleaned]
                skip_fields = [7, 8, 9, 10, 13]
                for idx, field in enumerate(fields):
                    if idx in skip_fields:
                        continue

                    field_class = field['class']

                    if 'mod-player' in field_class:
                        player_name = field.find('div', class_='text-of').text.strip()
                        new_row.append(players_dict[player_name])
                        new_row.append(player_name)
                        player_team = field.find('div', class_='ge-text-light').text.strip()
                        
                        #since team names in player stats are abbreviated, we need to check if the player's team is the winner or loser
                        #from map header to get the full team name, then get the team id from the teams_dict
                    
                        if player_team in map_entry[3]:
                            new_row.append(teams_dict[map_entry[3]]) #player is on the winning team
                            new_row.append(map_entry[3])
                        else:
                            new_row.append(teams_dict[map_entry[4]]) #player is on the losing team
                            new_row.append(map_entry[4])

                        

                        print(f"Player {field.find('div', class_='text-of').text.strip()}")
                        print(f"Team {field.find('div', class_='ge-text-light').text.strip()}")
                    elif 'mod-agents' in field_class:
                        hero_played = field.find('img').get('alt')
                        new_row.append(agents_dict[hero_played])
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


def get_player_and_match_stats(selenium_driver, df_match_details, df_map_details, df_players_stats, matches_info):
    
    for match_info_pair in matches_info:
        match_entry = get_match_details(match_info_pair, selenium_driver)
        df_match_details.loc[len(df_match_details)] = match_entry

        stats_container = selenium_driver.find_element(By.CLASS_NAME, 'vm-stats')
        maps = stats_container.find_elements(By.CLASS_NAME, 'vm-stats-gamesnav-item')
        
        for map in maps:
            df_players_stats = get_player_stats_on_map(selenium_driver, map, df_players_stats, df_map_details, match_entry[0])

        

    return df_match_details, df_map_details, df_players_stats