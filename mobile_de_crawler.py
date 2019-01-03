from crawler import Crawler
from selenium import webdriver
import os
import time

JSON_FILE_PATH = 'assets/MD.json'
CHROME_DRIVER_PATH = os.path.abspath('assets/chromedriver.exe')


class MdCrawler(Crawler):

    def __init__(self, start_url, source):
        super().__init__(start_url, source)
        serialized_arr = self.read_data_from_json_file(JSON_FILE_PATH)
        self.sent_ids = [] if serialized_arr is None else serialized_arr
        self.web_driver_chrome = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

    def get_page_content(self, url):
        self.web_driver_chrome.get(url)
        return self.web_driver_chrome.page_source

    def get_car_links(self, soup):
        urls = []
        for div in soup.find_all('div', {'class': 'dealerAd'}):
            urls.append(div.find('a')['href'])
        return urls

    def _get_next_page(self, soup):
        link = soup.find('span', {'class': 'btn btn--orange btn--s next-resultitems-page rbt-page-forward'})
        return self.start_url if link is None else link['data-href']

    def check_car_match(self, car_soup):
        try:
            url = car_soup.find('li', {'class': 'header-meta-action-dropdown-item u-text-nowrap'}).find('a')['href']
            img_url = car_soup.find('div', {
                'class': 'gallery-img-wrapper u-flex-centerer slick-slide slick-current slick-active'}).find('img')[
                'src']

            id = url.split('?')[1].split('&')[0].split('=')[1]
            price = car_soup.find('span', {'class': 'h3 rbt-prime-price'}).text

            title = car_soup.title.string

            km = car_soup.find('div', {'id': 'rbt-mileage-v'}).text
            first_registration = car_soup.find('div', {'id': 'rbt-firstRegistration-v'}).text
            if int(first_registration.split('/')[0]) < 3:
                print("> MobileDe: ID {id} is 2013 model".format(id=id))
                return

            mileage = car_soup.find('div', {'id': 'rbt-mileage-v'}).text
            emission = car_soup.find('div', {'id': 'rbt-emissionClass-v'}).text
            fuel = car_soup.find('div', {'id': 'rbt-fuel-v'}).text
            cubic = car_soup.find('div', {'id': 'rbt-cubicCapacity-v'}).text
            power = car_soup.find('div', {'id': 'rbt-power-v'}).text

            content = ' | '.join([title, price, km, first_registration, mileage, emission, fuel, cubic, power, self.shorten_url(url)])

            if id in self.sent_ids:
                print("> MobileDe: ID {id} is already sent".format(id=id))
                return

            if int(self.strip_non_alpha(price)) <= 12500:
                self.send_to_mobile(img_url)
                self.send_to_mobile(content)
                self.sent_ids.append(id)
                self.write_data_to_json_file(self.sent_ids, JSON_FILE_PATH)
                print("> MobileDe: sending ID {id}".format(id=id))

        except Exception as e:
            print(e)
            time.sleep(10)
