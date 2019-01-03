import time
import requests
import re
import json
import bs4
import threading
import telegram
import datetime

STATUS_REPORT_FREQ_SEC = 60000  # 10min

BITLY_TOKEN = '275309f31e21b25ef8de19d6314e255fcb05fb50'
TELEGRAM_TOKEN = '609324531:AAHbaORcfzybAVwlVhCrcivLdCRkcBppcKI'
TELEGRAM_CHAT_ID = '425134856'
TELEGRAM_APP_STATUS_TOKEN = '544747044:AAHPburosPia9uQLR4nEs7JD49QcCsj3yZY'
TELEGRAM_APP_STATUS_CHAT_ID = '425134856'


class Crawler(threading.Thread):

    def __init__(self, start_url, source):
        threading.Thread.__init__(self)
        self.source = source
        self.start_url = self.next_url = start_url
        self.sent_urls = []
        self.telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)
        self.telegram_app_status_bot = telegram.Bot(token=TELEGRAM_APP_STATUS_TOKEN)
        self.last_check = datetime.datetime.now()

    def run(self):
        while True:
            try:
                self.check_app_status()

                print('> [{source}] Visiting: {url}'.format(source=self.source, url=self.next_url))
                result_content = self.get_page_content(url=self.next_url)
                pagination_soup = bs4.BeautifulSoup(result_content, 'lxml')

                for car_url in self.get_car_links(pagination_soup):
                    print('> [{source}] Visiting car: {url}'.format(source=self.source, url=car_url))
                    result_content = self.get_page_content(url=car_url)
                    car_soup = bs4.BeautifulSoup(result_content, 'lxml')
                    self.check_car_match(car_soup)
                    time.sleep(.500)

                self.next_url = self._get_next_page(pagination_soup)
                if self.next_url == self.start_url:
                    print('> [{source}] Reached end of pagination page - sleeping 1 min'.format(source=self.source))
                    time.sleep(60)

            except Exception as e:
                print(e)

    def get_page_content(self, url):
        result = requests.get(url=url)
        return result.content

    # @abstractmethod
    def get_car_links(self, soup):
        print("Calling # @abstractmethod _get_car_links")
        return []

    # @abstractmethod
    def _get_next_page(self, soup):
        return None

    # @abstractmethod
    def check_car_match(self, car_soup):
        pass

    def send_to_mobile(self, content):
        try:
            self.telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=content)
            print('Successfully sent')
        except Exception as e:
            print(e)
            pass

    def check_app_status(self):
        if (datetime.datetime.now() - self.last_check).seconds >= STATUS_REPORT_FREQ_SEC:
            self.last_check = datetime.datetime.now()
            self.telegram_app_status_bot.send_message(chat_id=TELEGRAM_APP_STATUS_CHAT_ID, text="[{source}] @ {time}".format(source=self.source, time=self.last_check.strftime("%d.%m.%Y %H:%M:%S")))

    def strip_non_alpha(self, text):
        return re.sub("[^0-9]", "", text)

    def write_data_to_json_file(self, data, path):
        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def read_data_from_json_file(self, path):
        try:
            return json.loads(open(path).read())
        except FileNotFoundError:
            return None

    def shorten_url(self, url):
        endpoint = 'https://api-ssl.bitly.com/v3/shorten'
        response = requests.get(endpoint, params={
            'access_token': BITLY_TOKEN,
            'longUrl': url
        }, verify=True)

        data = response.json()
        if not data['status_code'] == 200:
            print(data)

        return data['data']['url']
