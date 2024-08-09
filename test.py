from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests

url = 'https://www.vlr.gg/event/matches/2095/champions-tour-2024-americas-stage-2/?series_id=4032'

# matches = requests.get(url)

# soup = BeautifulSoup(matches.text, 'html.parser')

# dates = soup.find_all('div', class_='wf-label mod-large')

# wf_cards = soup.find_all('div', class_='wf-card')


# def convertMonth(month):
#     if month == 'Jan':
#         return 1
#     elif month == 'Feb':
#         return 2
#     elif month == 'Mar':
#         return 3
#     elif month == 'Apr':
#         return 4
#     elif month == 'May':
#         return 5
#     elif month == 'Jun':
#         return 6
#     elif month == 'Jul':
#         return 7
#     elif month == 'Aug':
#         return 8
#     elif month == 'Sep':
#         return 9
#     elif month == 'Oct':
#         return 10
#     elif month == 'Nov':
#         return 11
#     elif month == 'Dec':
#         return 12

# for wf_card in wf_cards:
#     if wf_card.previous_sibling.previous_sibling is not None:
#         date_raw = wf_card.previous_sibling.previous_sibling.text.strip()
#         numerical_date = date_raw.split(',')[1:]
#         # month, day = numerical_date[0].split(' ')
#         # month = convertMonth(month)
#         # print(f"{month}/{day}/{numerical_date[2]}")
#         print(numerical_date)
#     links = wf_card.find_all('a')
#     for link in links:
#         print(link['href'])

base_url = 'https://www.vlr.gg/'

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

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
            
            # print(numerical_date)

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

matches = get_matches_dates_and_urls(requests.get(url))
print(matches)
print(len(matches))
print(matches[0][0])
print(matches[0][1])
    