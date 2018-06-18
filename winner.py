
from methods import get_google_winner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import time
import json
import logging
import random


class GoogleWinnerSpider():
    name = 'winnerspider'

    matches = {
        # 'russia-v-saudi-arabia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt317s;2;/m/030q7;dt;fp;1',
        # 'egypt-v-uruguay': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb34yxg;2;/m/030q7;dt;fp;1',
        # 'morocco-v-iran': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35h86;2;/m/030q7;dt;fp;1',
        # 'portugal-v-spain': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdw869;2;/m/030q7;dt;fp;1',
        # 'france-v-australia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt2vmy;2;/m/030q7;dt;fp;1',
        # 'argentina-v-iceland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt1vkz;2;/m/030q7;dt;fp;1',
        # 'peru-v-denmark': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&#sie=m;/g/11f4qdwwxc;2;/m/030q7;dt;fp;1',
        # 'croatia-v-nigeria': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdwkfv;2;/m/030q7;dt;fp;1',
        # 'costa-rica-v-serbia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt3dsw;2;/m/030q7;dt;fp;1',
        # 'germany-v-mexico': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt3cf0;2;/m/030q7;dt;fp;1',
        'brazil-v-switzerland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f62zwxrr;2;/m/030q7;dt;fp;1',
        # 'sweden-v-south-korea': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb361_w;2;/m/030q7;dt;fp;1',
        # 'belgium-v-panama': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdx1m0;2;/m/030q7;dt;fp;1',
        # 'tunisia-v-england': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt3znf;2;/m/030q7;dt;fp;1',
        #'poland-v-senegal': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdw6t5;2;/m/030q7;dt;fp;1',
        #'colombia-v-japan': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb34l7j;2;/m/030q7;dt;fp;1',
        #'russia-v-egypt': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35nz7;2;/m/030q7;dt;fp;1',
        # 'portugal-v-morocco': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35wnq;2;/m/030q7;dt;fp;1',
        # 'uruguay-v-saudi-arabia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdxbrf;2;/m/030q7;dt;fp;1',
        # 'iran-v-spain': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdw60b;2;/m/030q7;dt;fp;1',
        # 'france-v-peru': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt2sjc;2;/m/030q7;dt;fp;1',
        # 'denmark-v-australia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35rz5;2;/m/030q7;dt;fp;1',
        # 'argentina-v-croatia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt2b7w;2;/m/030q7;dt;fp;1',
        # 'brazil-v-costa-rica': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdx7vy;2;/m/030q7;dt;fp;1',
        # 'nigeria-v-iceland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdw3fg;2;/m/030q7;dt;fp;1',
        # 'serbia-v-switzerland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35w6w;2;/m/030q7;dt;fp;1',
        # 'belgium-v-tunisia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35rz3;2;/m/030q7;dt;fp;1',
        # 'germany-v-sweden': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdwgr3;2;/m/030q7;dt;fp;1',
        # 'south-korea-v-mexico': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35qpd;2;/m/030q7;dt;fp;1',
        # 'england-v-panama': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb356pk;2;/m/030q7;dt;fp;1',
        # 'japan-v-senegal': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qd_7gl;2;/m/030q7;dt;fp;1',
        # 'poland-v-colombia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdwkfj;2;/m/030q7;dt;fp;1',
        # 'saudi-arabia-v-egypt': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdx0vf;2;/m/030q7;dt;fp;1',
        # 'uruguay-v-russia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb350j3;2;/m/030q7;dt;fp;1',
        # 'iran-v-portugal': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdwcl0;2;/m/030q7;dt;fp;1',
        # 'spain-v-morocco': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdx50_;2;/m/030q7;dt;fp;1',
        # 'australia-v-peru': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdx2wc;2;/m/030q7;dt;fp;1',
        # 'denmark-v-france': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt1pz5;2;/m/030q7;dt;fp;1',
        # 'iceland-v-croatia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdw6tn;2;/m/030q7;dt;fp;1',
        # 'nigeria-v-argentina': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdv48r;2;/m/030q7;dt;fp;1',
        # 'mexico-v-sweden': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35q6f;2;/m/030q7;dt;fp;1',
        # 'south-korea-v-germany': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11ggb35jf0;2;/m/030q7;dt;fp;1',
        # 'serbia-v-brazil': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdwvqg;2;/m/030q7;dt;fp;1',
        # 'switzerland-v-costa-rica': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdvvfs;2;/m/030q7;dt;fp;1',
        # 'japan-v-poland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11hcjt1rrx;2;/m/030q7;dt;fp;1',
        # 'senegal-v-colombia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdwcl2;2;/m/030q7;dt;fp;1',
        # 'england-v-belgium': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdwt66;2;/m/030q7;dt;fp;1',
        # 'panama-v-tunisia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018#sie=m;/g/11f4qdx8kb;2;/m/030q7;dt;fp;1'
    }

    def __init__(self):

        # Make chrome invisible
        # display = Display(visible=0, size=(800, 600))
        # display.start()

        self.driver = webdriver.Chrome()
        self.logger = logging.getLogger(self.name)

        self.result_file = open("winner.json", 'w')

    def make_requests(self):

        results = []

        for match_name, url in self.matches.items():
            print(url)

            self.driver.get(url)
            webdriver_wait = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "tb_view Hr51pb"))
            )
            self.logger.info(webdriver_wait)

            winner_json = get_google_winner(self.driver, self.driver.page_source, match_name)

            results.append(winner_json)
            print('**** SUCCESSFULLY CRAWL: %s ****' % match_name)

            print(winner_json)
            self.driver.quit()
            self.driver = webdriver.Chrome()
            time.sleep(5)

        self.driver.quit()
        json.dump(results, self.result_file)
        self.result_file.close()


if __name__ == '__main__':
    spider = GoogleWinnerSpider()
    spider.make_requests()
