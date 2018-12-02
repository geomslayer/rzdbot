# coding: utf-8

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options


class Checker:
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.set_script_timeout(10)
        self.driver.set_page_load_timeout(10)

    def check_seats(self, train, date):
        try:
            url = train.url.format(date=date)
            self.driver.get(url)
        except TimeoutException:
            return False
        # sleeping because of selenium's weird behavior
        time.sleep(5)
        route_items = self.driver.find_elements_by_class_name('route-item')
        for item in route_items:
            train_id = item.find_element_by_css_selector('.route-trtitle-row .route-trnum').text.strip().lower()
            if train.id != train_id:
                continue
            for car_type in item.find_elements_by_class_name('route-carType-item'):
                seat_type = car_type.find_element_by_class_name('serv-cat').text.strip().lower()
                if seat_type in train.seat_types:
                    return True
        return False


def main():
    from config import TRAINS

    checker = Checker()
    print(checker.check_seats(TRAINS[0], TRAINS[0].dates[0]))

    time.sleep(60)


if __name__ == '__main__':
    main()
