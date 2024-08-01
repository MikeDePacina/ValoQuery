from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()

# url = 'https://www.vlr.gg/365316/gen-g-vs-rex-regum-qeon-champions-tour-2024-pacific-stage-2-ko/?game=all&tab=overview'
url = 'https://www.vlr.gg/314340/zeta-division-vs-drx-champions-tour-2024-pacific-stage-2-w1'

vct_apac_matches = 'https://www.vlr.gg/event/matches/2005/champions-tour-2024-pacific-stage-2/?series_id=3839'

csv_columns = [
               "MatchID",
               "Match Date",
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

df = pd.DataFrame(columns=csv_columns)

driver.get(url)

#wait 1s for page to load
driver.implicitly_wait(1)

stats_container = driver.find_element(By.CLASS_NAME, 'vm-stats')
maps = stats_container.find_elements(By.CLASS_NAME, 'vm-stats-gamesnav-item')

#skip all maps overview
match_id = 0
for map in maps[1]:
    
    #skip if map is disabled, match already concluded
    if 'mod-disabled' in map.get_attribute('class'):
        continue

    map.click()
    driver.implicitly_wait(0.5)
    
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    map_name = soup.find('div', class_='vm-stats-gamesnav-item js-map-switch mod-active').text.strip()
    map_name_cleaned = map_name.split('\n')[2].replace('\t','')
    
    map_stats = soup.find('div', class_='vm-stats-container')
    teams_stats_table = map_stats.find_all('table', class_='wf-table-inset mod-overview')

    

    for team_stats_table in teams_stats_table:
        for i, row in enumerate(team_stats_table.find_all('tr')):
            if i == 0:
                continue #skip header row
            else:
                fields = row.find_all('td')
                new_row = [match_id, map_name_cleaned]
                for idx, field in enumerate(fields):
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
                new_row = []
            