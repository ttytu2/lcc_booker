# -*- coding: utf-8 -*-

from booker.booker_factory import BookerFactory
from _webdriver_info import WebDriverInfo


class BookerEngine:
    def __init__(self):
        pass

    def run(self, booker_req):
        booker = BookerFactory.newBooker(booker_req)
        if booker_req.browser == 'Chrome':
            driver = WebDriverInfo(booker_req, 1)
        else:
            driver = WebDriverInfo(2)
        driver = driver.browser
        result = booker.get_booker_result(driver, booker_req)
        driver.quit()

        return result
