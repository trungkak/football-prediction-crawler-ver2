
from methods import get_oneeighteight
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import logging
import json
import time
import random


class OneEightEightSpider():
    name = "188spider"

    def __init__(self):

        self.start_urls = ["https://www.mot88bet.com/vi-vn/world-cup#06" + str(i) for i in range(18, 30)]

        # Make chrome invisible
        display = Display(visible=0, size=(800, 600))
        display.start()

        self.driver = webdriver.Chrome()
        self.logger = logging.getLogger(self.name)

        self.result_file = open("188.json", 'w')

    def __del__(self):
        self.logger.info('quitting driver')
        self.driver.quit()

    def make_requests(self):

        results = []

        for url in self.start_urls:
            print(url)
            try:
                self.driver.get(url)
                webdriver_wait = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "bet-types-table"))
                )
                self.logger.info(webdriver_wait)
            except Exception:
                self.logger.info('EXCEPTION')
                # self.driver.quit()
                continue

            raw_data_list = get_oneeighteight(self.driver.page_source, match_name=url)
            result = []

            # Country name dictionary
            with open('countries_names.json') as countries_name:
                countries_name_dict = json.load(countries_name)

            # parse raw data
            matches_data = [raw_data_list[i:i + 3] for i in range(0, len(raw_data_list), 3)]

            for match_data in matches_data:
                team1_data = match_data[0]
                team2_data = match_data[1]
                draw_data = match_data[2]

                match_data_json = {}
                match_data_json['MATCHNAME'] = {}
                if team1_data[0].strip().title() in countries_name_dict:
                    match_data_json['MATCHNAME']['team1'] = countries_name_dict[team1_data[0].strip().title()]
                else:
                    match_data_json['MATCHNAME']['team1'] = team1_data[0].strip().title()

                if team2_data[0].strip().title() in countries_name_dict:
                    match_data_json['MATCHNAME']['team2'] = countries_name_dict[team2_data[0].strip().title()]
                else:
                    match_data_json['MATCHNAME']['team2'] = team2_data[0].strip().title()

                match_data_json['CATRAN-onextwo'] = {}
                match_data_json['CATRAN-onextwo']['team1'] = [team1_data[1]]
                match_data_json['CATRAN-onextwo']['team2'] = [team2_data[1]]
                match_data_json['CATRAN-onextwo']['draw'] = [draw_data[1]]

                match_data_json['CATRAN-handicap'] = {}
                match_data_json['CATRAN-handicap']['team1'] = [team1_data[2].split()[0], team1_data[2].split()[1]]
                match_data_json['CATRAN-handicap']['team2'] = [team2_data[2].split()[0], team2_data[2].split()[1]]

                match_data_json['CATRAN-underover'] = {}
                match_data_json['CATRAN-underover']['team1'] = [' '.join(team1_data[3].split()[:2]),
                                                                team1_data[3].split()[2]]
                match_data_json['CATRAN-underover']['team2'] = [' '.join(team2_data[3].split()[:2]),
                                                                team2_data[3].split()[2]]

                match_data_json['HIEP1-onextwo'] = {}
                match_data_json['HIEP1-onextwo']['team1'] = [team1_data[1 + 3]]
                match_data_json['HIEP1-onextwo']['team2'] = [team2_data[1 + 3]]
                match_data_json['HIEP1-onextwo']['draw'] = [draw_data[2]]

                match_data_json['HIEP1-handicap'] = {}
                match_data_json['HIEP1-handicap']['team1'] = [team1_data[2 + 3].split()[0],
                                                              team1_data[2 + 3].split()[1]]
                match_data_json['HIEP1-handicap']['team2'] = [team2_data[2 + 3].split()[0],
                                                              team2_data[2 + 3].split()[1]]

                match_data_json['HIEP1-underover'] = {}
                match_data_json['HIEP1-underover']['team1'] = [' '.join(team1_data[3 + 3].split()[:2]),
                                                               team1_data[3 + 3].split()[2]]
                match_data_json['HIEP1-underover']['team2'] = [' '.join(team2_data[3 + 3].split()[:2]),
                                                               team2_data[3 + 3].split()[2]]

                match_data_json['DATETIME'] = 'Undefined'

                result.append(match_data_json)

            print(result)

            results.append(result)
            time.sleep(random.randint(2, 5))

        json.dump(results, self.result_file)
        self.driver.quit()


if __name__ == '__main__':
    spider = OneEightEightSpider()
    spider.make_requests()