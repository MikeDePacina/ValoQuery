from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests

url = 'https://www.vlr.gg/365318/paper-rex-vs-gen-g-champions-tour-2024-pacific-stage-2-ubsf'

driver = webdriver.Chrome()

driver.get(url)

   
driver.implicitly_wait(1)

match_id = 0

#populate match df
match_row = [match_id]

match_header = driver.find_element(By.CLASS_NAME, 'match-header-vs')
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
picks_and_bans = driver.find_element(By.CLASS_NAME, 'match-header-note').text

match_row.append(winner)
match_row.append(loser)
match_row.append(winner_score)
match_row.append(loser_score)
match_row.append(picks_and_bans)

print(match_row)