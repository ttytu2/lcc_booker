# -*- coding: utf-8 -*-
import json
import time
import logging
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from booker._9C._db.dao_mysql import DaoMysql
from create_order_process import CreateOrderProcess
from conf import booker_config


class SpringAirlines(object):
    logger = logging.getLogger()

    @staticmethod
    def get_booker_url(req):

        urlPath = 'https://flights.ch.com/' + req.fromCity + '-' + req.toCity + '.html?'

        # zh-CN
        basePara = 'Departure={0}&Arrival={1}&FDate={2}&ANum={3}'.format(
            req.fromCity, req.toCity, req.startTime, req.adultNumber)
        result = urlPath + basePara

        if req.flightOption == 2:
            result = result + '&RetDate={0}&IfRet=true'.format(req.endTime)

        if req.childNumber > 0:
            result = result + '&CNum={0}'.format(req.childNumber)

        logging.info('shopping url:%s', result)

        return result

    @staticmethod
    def do_booker_login(browser, account):
        url = 'https://passport.ch.com/zh_cn/Login/NormalPC'
        browser.get(url)

        element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
            EC.visibility_of_element_located((By.NAME, "UserNameInput"))
        )

        username = account["username"]
        password = account["password"]
        browser.find_element_by_name("UserNameInput").send_keys(username)
        browser.find_element_by_name("PasswordInput").send_keys(password)
        browser.find_element_by_id("account-submit").click()
        time.sleep(3)
        if browser.current_url == url:
            browser.execute_script('$("#u-loading-layer").css("display","none")')
            browser.find_element_by_id("account-submit").click()

    def get_booker_result(self, browser, req):
        account = DaoMysql.get_available_account()
        # 登录
        self.do_booker_login(browser, account)
        time.sleep(3)
        browser.get(self.get_booker_url(req))

        # noinspection PyBroadException
        try:
            # 判断航班号
            CreateOrderProcess.confirm_flightNumber(browser, req)
        except Exception as e:
            browser.get_screenshot_as_file("/tmp/" + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.png'))
            self.logger.error("flightnumber exception: {0}".format(e), exc_info=1)
            result = {"status": "1", "message": "No flight number found or Jump"}
            return result

        try:
            # 填写所有乘客信息
            CreateOrderProcess.fill_in_information(browser, req)
        except Exception as e:
            browser.get_screenshot_as_file("/tmp/" + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.png'))
            self.logger.error("passenger exception: {0}".format(e), exc_info=1)
            result = {"status": "2",
                      "message": "Passenger information is wrong and username:%s" % (account["username"])}
            return result

        try:
            # 所有增值业务设置为不选取 确认订单
            CreateOrderProcess.confirmation_information(browser, req)
        except Exception as e:
            browser.get_screenshot_as_file("/tmp/" + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.png'))
            self.logger.error("ssr exception: {0}".format(e), exc_info=1)
            result = {"status": "3", "message": "Confirm the order is wrong and username:%s" % (account["username"])}
            return result
        try:
            u_dialog_msg = WebDriverWait(browser, 1).until(
                EC.visibility_of_element_located((By.ID, 'u-dialog-msg')))
            if u_dialog_msg:
                browser.get_screenshot_as_file("/tmp/" + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.png'))
                text = (u_dialog_msg.get_attribute('textContent').encode("utf-8"))
                # self.logger.warn(": {0}".format(json.dumps(req)))
                if text.find("限制") >= 0:
                    result = {"status": "4",
                              "message": u_dialog_msg.get_attribute('textContent') + " and username:%s" % (
                                  account["username"])}
                    DaoMysql.change_account_disabled(account["username"])
                    return result
                result = {"status": "6", "message": u_dialog_msg.get_attribute('textContent') + " and username:%s" % (
                    account["username"])}
                return result
        except:
            browser.get_screenshot_as_file("/tmp/" + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.png'))
            pass
        try:
            element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'w-main'))
            )
            order_number = browser.find_element_by_class_name("w-main").find_element_by_class_name("col-orange").text
            order_price = browser.find_element_by_class_name("price-num").text
        except Exception as e:
            browser.get_screenshot_as_file("/tmp/" + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.png'))
            self.logger.error("submit exception: {0}".format(e), exc_info=1)
            result = {"status": "7", "message": "未知错误 and username:%s" % (account["username"])}
            return result

        result = {"status": "0", "message": "Order successfully created", "orderNumber": order_number,
                  "orderPrice": order_price, "orderUsername": account["username"], "orderPassword": account["password"]}

        self.logger.debug(result)

        return result
