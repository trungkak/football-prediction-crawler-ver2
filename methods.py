
import pandas as pd
from scrapy.selector import Selector
from datetime import datetime
from bs4 import BeautifulSoup, Comment


def get_google_winner(driver, source, title):
    winning_percents = {}
    team_names = title.split('-v-')
    team1 = ' '.join(team_names[0].split('-'))
    team2 = ' '.join(team_names[1].split('-'))

    # lis = driver.find_elements_by_tag_name('li')

    # for li in lis:
    #     if li.text == 'ĐỘI HÌNH RA SÂN':
    #         print(li)
    #         li.click()
    #         break

    # source = driver.page_source
    soup = BeautifulSoup(source, "lxml")

    try:
        team1_percent = Selector(text=source) \
            .xpath('//*[@id="match-stats"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/text()') \
            .extract()[0]
    except:
        team1_percent = 'ERROR'

    try:
        draw_percent = Selector(text=source) \
            .xpath('//*[@id="match-stats"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[2]/text()') \
            .extract()[0]
    except:
        draw_percent = 'ERROR'

    try:
        team2_percent = Selector(text=source) \
            .xpath('//*[@id="match-stats"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[3]/text()') \
            .extract()[0]
    except:
        team2_percent = 'ERROR'

    try:
        match_score_div = soup.find('div', class_ = "imso_mh__ma-sc-cont")
        match_score = ' '.join(match_score_div.find_all(text=True))[:3]
    except:
        match_score = 'ERROR'

    try:
        match_time_div = soup.find('div', class_ = "imso_mh__lv-m-stts-cont")
        match_time = ' '.join(match_time_div.find_all(text=True))[:2].strip()
    except:
        if match_score != 'ERROR':
            match_time = 'MATCHOVER'
        else:
            match_time = 'ERROR'

    lineups_div = soup.find('div', class_ = "lineup-section")

    team_lineup = {
        'team1': {},
        'team2': {}
    }
    if lineups_div:
        try:
            all_players = ' '.join([div.text for div in soup.find_all('span', class_="jersey-num-cell")])
            team_lineup['team1']['players'] = all_players.split()[:11]
            team_lineup['team2']['players'] = all_players.split()[11:]

            print(team_lineup['team1']['players'])
            print(team_lineup['team2']['players'])

            all_formations = ' '.join(
                [div.text for div in soup.find_all('span', class_="oEwJQ tBpa2 text-middle formation")])
            print(all_formations)
            team_lineup['team1']['lineup'] = all_formations.split()[0]
            team_lineup['team2']['lineup'] = all_formations.split()[1]
        except:
            print('MATCH NOT STARTED')

    winning_percents[team1] = team1_percent
    winning_percents['draw'] = draw_percent
    winning_percents[team2] = team2_percent
    winning_percents['first_team'] = team1
    winning_percents['second_team'] = team2

    if match_score != 'ERROR' and match_time != 'ERROR':
        winning_percents['match_score'] = match_score
        winning_percents['match_time'] = match_time

    if team_lineup['team1'] != {}:
        winning_percents['lineups'] = team_lineup

    return winning_percents


# Keo nha cai data

def get_oneeighteight(source, match_name):
    soup = BeautifulSoup(source, "lxml")
    bet_tables = soup.find_all("table", class_="bet-types-table")

    matches = []

    names = []

    for bet_table in bet_tables:
        table_rows = bet_table.find('tbody').find_all('tr', recursive=False)[2:] # Cause 2 first tr is metadata
        for table_row in table_rows:
            tds = table_row.find_all('td', recursive=False)
            # row_data = [td.text for td in tds if td.text.strip() != '']
            row_data = [' '.join(td.find_all(text=lambda text: not isinstance(text, Comment))) for td in tds if td.text.strip() != '']
            matches.append(row_data)
    print('*** ' + match_name + ' ***')
    return matches
