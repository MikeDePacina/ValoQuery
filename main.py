from selenium import webdriver
import pandas as pd
import requests
from utils import player_stats_columns, match_columns, map_columns
from urls import vct_apac_matches, vct_americas_matches, vct_emea_matches, vct_china_matches
from scrappers import get_matches_dates_and_urls, get_player_and_match_stats

global_driver = webdriver.Chrome()

vct_apac_matches_html = requests.get(vct_apac_matches)
vct_americas_matches_html = requests.get(vct_americas_matches)
vct_emea_matches_html = requests.get(vct_emea_matches)
vct_china_matches_html = requests.get(vct_china_matches)

vct_apac_matches_info = get_matches_dates_and_urls(vct_apac_matches_html)
vct_americas_matches_info = get_matches_dates_and_urls(vct_americas_matches_html)
vct_emea_matches_info = get_matches_dates_and_urls(vct_emea_matches_html)
vct_china_matches_info = get_matches_dates_and_urls(vct_china_matches_html)

df_vct_apac_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_apac_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)
df_vct_apac_season2_playoffs_map_details = pd.DataFrame(columns=map_columns)

df_vct_americas_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_americas_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)
df_vct_americas_season2_playoffs_map_details = pd.DataFrame(columns=map_columns)

df_vct_emea_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_emea_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)
df_vct_emea_season2_playoffs_map_details = pd.DataFrame(columns=map_columns)

df_vct_china_season2_playoffs_player_stats = pd.DataFrame(columns=player_stats_columns)
df_vct_china_season2_playoffs_match_details = pd.DataFrame(columns=match_columns)
df_vct_china_season2_playoffs_map_details = pd.DataFrame(columns=map_columns)


df_vct_americas_season2_playoffs_match_details, df_vct_americas_season2_playoffs_map_details, df_vct_americas_season2_playoffs_player_stats = get_player_and_match_stats(
                                                                                                                global_driver,
                                                                                                                df_vct_americas_season2_playoffs_match_details, 
                                                                                                                df_vct_americas_season2_playoffs_map_details,
                                                                                                                df_vct_americas_season2_playoffs_player_stats, 
                                                                                                                vct_americas_matches_info)

df_vct_apac_season2_playoffs_match_details, df_vct_apac_season2_playoffs_map_details, df_vct_apac_season2_playoffs_player_stats = get_player_and_match_stats(
                                                                                                                global_driver,
                                                                                                                df_vct_apac_season2_playoffs_match_details, 
                                                                                                                df_vct_apac_season2_playoffs_map_details,
                                                                                                                df_vct_apac_season2_playoffs_player_stats,
                                                                                                                vct_apac_matches_info)

df_vct_emea_season2_playoffs_match_details, df_vct_emea_season2_playoffs_map_details, df_vct_emea_season2_playoffs_player_stats = get_player_and_match_stats(
                                                                                                                global_driver,
                                                                                                                df_vct_emea_season2_playoffs_match_details,
                                                                                                                df_vct_emea_season2_playoffs_map_details,
                                                                                                                df_vct_emea_season2_playoffs_player_stats,
                                                                                                                vct_emea_matches_info)

df_vct_china_season2_playoffs_match_details, df_vct_china_season2_playoffs_map_details, df_vct_china_season2_playoffs_player_stats = get_player_and_match_stats(
                                                                                                                global_driver,
                                                                                                                df_vct_china_season2_playoffs_match_details,
                                                                                                                df_vct_china_season2_playoffs_map_details,
                                                                                                                df_vct_china_season2_playoffs_player_stats,
                                                                                                                vct_china_matches_info)
    
global_driver.quit()

df_vct_americas_season2_playoffs_match_details.to_csv('./csvs/vct_americas_season2_stage2_playoffs_match_details.csv', index=False)
df_vct_americas_season2_playoffs_map_details.to_csv('./csvs/vct_americas_season2_stage2_playoffs_map_details.csv', index=False)
df_vct_americas_season2_playoffs_player_stats.to_csv('./csvs/vct_americas_season2_stage2_playoffs_player_stats.csv', index=False)

df_vct_apac_season2_playoffs_match_details.to_csv('./csvs/vct_apac_season2_playoffs_match_details.csv', index=False)
df_vct_apac_season2_playoffs_map_details.to_csv('./csvs/vct_apac_season2_playoffs_map_details.csv', index=False)
df_vct_apac_season2_playoffs_player_stats.to_csv('./csvs/vct_apac_season2_playoffs_player_stats.csv', index=False)

df_vct_emea_season2_playoffs_match_details.to_csv('./csvs/vct_emea_season2_playoffs_match_details.csv', index=False)
df_vct_emea_season2_playoffs_map_details.to_csv('./csvs/vct_emea_season2_playoffs_map_details.csv', index=False)
df_vct_emea_season2_playoffs_player_stats.to_csv('./csvs/vct_emea_season2_playoffs_player_stats.csv', index=False)

df_vct_china_season2_playoffs_match_details.to_csv('./csvs/vct_china_season2_playoffs_match_details.csv', index=False)
df_vct_china_season2_playoffs_map_details.to_csv('./csvs/vct_china_season2_playoffs_map_details.csv', index=False)
df_vct_china_season2_playoffs_player_stats.to_csv('./csvs/vct_china_season2_playoffs_player_stats.csv', index=False)
   



