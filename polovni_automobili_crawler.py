from crawler import Crawler
from time import sleep

JSON_FILE_PATH = 'assets/PA.json'


class PaCrawler(Crawler):

    def __init__(self, start_url, source):
        super().__init__(start_url, source)
        serialized_arr = self.read_data_from_json_file(JSON_FILE_PATH)
        self.sent_ids = [] if serialized_arr is None else serialized_arr

    def get_car_links(self, soup):
        urls = []
        for a in soup.find_all('a', {'class': 'ga-title'}):
            if "bmw" in a['href']:
                urls.append('https://www.polovniautomobili.com' + a['href'])
        return urls

    def _get_next_page(self, soup):
        link = soup.find('a', {'class': 'js-pagination-next'})
        return self.start_url if link is None else 'https://www.polovniautomobili.com' + link['href']

    def check_car_match(self, car_soup):
        try:
            url = car_soup.find('link', {'rel': 'canonical'})['href']
            img_url = car_soup.find('ul', {'id': 'image-gallery'}).find('li').find('img')['src']

            id = url.split('/')[-2]
            price = car_soup.find('div', {'id': 'not-cached-holder'})['data-title'].split(' - ')[-1]

            content_divs = car_soup.find_all('div', {'class': 'uk-width-large-1-1 uk-width-medium-3-10 uk-width-1-2'})
            content_tags = [div.text for div in content_divs]
            content_tags.append(price)
            content_tags.append(self.shorten_url(url))
            content = ' | '.join(content_tags)

            if id in self.sent_ids:
                print("> PolovniAutomobili ID {id} is already sent".format(id=id))
                return

            if int(self.strip_non_alpha(price)) <= 15000:
                # self.send_to_mobile(img_url)
                self.send_to_mobile(content)
                self.sent_ids.append(id)
                self.write_data_to_json_file(self.sent_ids, JSON_FILE_PATH)
                print('> PolovniAutomobili Sending message for ID: ' + id)

        except Exception as e:
            print(e)
            sleep(10)
