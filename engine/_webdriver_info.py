# -*- coding: UTF-8 -*-
from selenium import webdriver
from engine._proxy_settings import get_chrome_proxy_extension
from conf import booker_config


class WebDriverInfo(object):
    status = 0
    browser = None
    type = 1  # 1: Chrome, 2: Firefox

    def __init__(self, booker_req, type=1, status=1):
        self.status = 1
        self.type = type

        if self.type == 1:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("window-size=3840,2160")
            chrome_options.set_headless()
            # # 如果是IT则加上代理
            # if booker_req.ipcc == "IT_F":
            #     chrome_options.add_extension(
            #         get_chrome_proxy_extension(booker_config.get('proxy1', 'dynamicProxy')))
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)

            self.browser = webdriver.Chrome(booker_config.get('browser', 'chromedriver'), chrome_options=chrome_options)
        elif self.type == 2:
            self.browser = webdriver.Firefox()
