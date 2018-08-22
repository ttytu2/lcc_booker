# -*- coding: utf-8 -*-
import logging
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from conf import booker_config


class TigerAirTw(object):
    logger = logging.getLogger()

    @staticmethod
    def get_booker_url(req):

        urlPath = 'https://booking.tigerairtw.com/?dlType=fltsrch&culture=zh-TW&pc=&extraDays=3'

        # zh-CN
        # basePara = '&psgr={0}_{1}_0=&origin={2}&dest={3}&depDate={4}&retDate={5}'.format(
        #     req.adultNumber, req.childNumber, req.fromCity, req.toCity, req.startTime, req.endTime)

        basePara = '&psgr={0}_{1}_0=&origin={2}&dest={3}&depDate={4}&retDate={5}'.format(
            1, 0, req.fromCity, req.toCity, req.startTime, req.endTime)
        result = urlPath + basePara

        if req.flightOption == 2:
            result = result + '&ms=RoundTrip'
        else:
            result = result + '&ms=Oneway'

        logging.info('shopping url:%s', result)

        return result

    def get_booker_result(self, driver, req):

        driver.get(self.get_booker_url(req))
        time.sleep(5)
        try:
            # 判断航班号
            confirm_flightNumber(driver, req)
        except Exception as e:
            self.logger.error("flightnumber exception: {0}".format(e), exc_info=1)
            result = {"status": "1", "message": "No flight number found or Jump"}
            return result
        """
        旅客资料填写
        """
        try:
            # 填写所有乘客信息
            fill_in_information(driver, req)
        except Exception as e:
            self.logger.error("passenger exception: {0}".format(e), exc_info=1)
            result = {"status": "2",
                      "message": "Passenger information is wrong "}
            return result
        try:
            # 选座位
            choose_seat(driver)
        except Exception as e:
            self.logger.error("passenger exception: {0}".format(e), exc_info=1)
            result = {"status": "3",
                      "message": "Choose seat fail"}
            return result

        try:
            # 信用卡付款
            creditcard_payment(driver, req)
        except Exception as e:
            self.logger.error("payment exception: {0}".format(e), exc_info=1)
            result = {"status": "5", "message": "Payment exception"}
            return result

        result = {"status": "0", "message": "Order successfully created"}

        self.logger.debug(result)
        return result


def confirm_flightNumber(driver, req):
    """
    判断航班号
    :param driver:
    :param req:
    :return:
    """
    flightNumbers = driver.find_elements_by_class_name("journey-details")
    for flightNumber in flightNumbers:
        if flightNumber.find_element_by_class_name("flight-number").text == req.fromSegments[0]["flightNumber"]:
            flightNumber.find_elements_by_class_name("md-half-lr-p")[0].click()
    time.sleep(4)
    driver.find_elements_by_class_name("btn-nav")[1].click()
    time.sleep(10)


def fill_in_information(driver, req):
    """
    旅客资料填写
    :param driver:
    :param req:
    :return:
    """
    sex_choice = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[1]/div[1]/div/div/button')
    ActionChains(driver).click(sex_choice).perform()
    driver.implicitly_wait(3)
    # 性别
    if req.passengers[0]["gender"] == "F":
        sex1 = u"MS"  # 1为 先生
    elif req.passengers[0]["gender"] == "M":
        sex1 = u"MR"
    sex_one = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[1]/div[1]/div/div/select')
    Select(sex_one).select_by_value(sex1)
    # 姓名
    first_name = req.passengers[0]["firstName"]
    second_name = req.passengers[0]["lastName"]
    driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/input').send_keys(second_name)
    driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[1]/div[3]/div/input').send_keys(first_name)

    # 国家
    country_select = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div/select')
    Select(country_select).select_by_value(req.passengers[0]["nationality"])
    """
    出生日期
    """
    birthday = req.passengers[0]["birthday"].split("-")
    # 年
    s_year = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[1]/div[4]/div/div[1]/div/select')
    Select(s_year).select_by_value(birthday[0])
    # 月
    s_month = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[1]/div[4]/div/div[2]/div/select')
    Select(s_month).select_by_value(birthday[1])
    # 日
    s_day = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[1]/div[4]/div/div[3]/div/select')
    Select(s_day).select_by_value(birthday[2])
    """
    到 期日
    """
    cardExpired = req.passengers[0]["cardExpired"].split("-")
    # 年
    d_year = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[2]/div[4]/div/div[1]/div/select')
    Select(d_year).select_by_value(cardExpired[0])
    # 月
    d_month = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[2]/div[4]/div/div[2]/div/select')
    Select(d_month).select_by_value(cardExpired[1])
    # 日
    d_day = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[2]/div[4]/div/div[3]/div/select')
    Select(d_day).select_by_value(cardExpired[2])
    cardNum = req.passengers[0]["cardNum"]
    # 护照
    id_number = driver.find_element_by_xpath(
        u'//*[@id="adult-1"]/div/div[1]/div/div[2]/div/div[2]/div[3]/div/input').send_keys(cardNum)
    driver.implicitly_wait(30)

    # 行李
    driver.find_element_by_xpath(u'//*[@id="baggage-segment-1-adult-1-BG00"]').click()
    time.sleep(7)

    # 保险框 不买保险
    js = u'var q=document.documentElement.scrollTop=10000'
    driver.execute_script(js)

    driver.find_element_by_xpath(
        u'//*[@id="root"]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/a').click()
    driver.find_element_by_xpath(
        u'//*[@id="root"]/div/div[2]/div/div[3]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/div[3]/a[2]').click()


def choose_seat(driver):
    """
    选座位
    :param driver:
    :return:
    """
    # 选座位界面   下拉到网页底部
    time.sleep(7)
    js_1 = u'var q=document.documentElement.scrollTop=10000'
    driver.execute_script(js_1)

    # 找到继续button
    jixu2 = driver.find_element_by_xpath(u'//*[@id="root"]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/a')
    ActionChains(driver).click(jixu2).perform()

    # 选座位界面 继续下一步
    time.sleep(4)
    click_jixu = driver.find_element_by_xpath(
        u'//*[@id="root"]/div/div[2]/div/div[3]/div[2]/div[1]/div/div/div[1]/div/div/div[3]/a[2]')
    ActionChains(driver).click(click_jixu).perform()


def creditcard_payment(driver, req):
    """
    联系人填写 与 信用卡支付
    :param driver:
    :param req:
    :return:
    """
    link_phone = booker_config.get('linkManInfo', 'phone')
    link_email = booker_config.get('linkManInfo', 'email')

    # 性别
    if req.passengers[0]["gender"] == "F":
        sex = u"MS"  # 1为 先生
    elif req.passengers[0]["gender"] == "M":
        sex = u"MR"
    sex_two = driver.find_element_by_xpath(
        u'//*[@id="root"]/div/div[2]/div/div[3]/div[2]/div[1]/div/div/div[1]'
        u'/div/div[2]/div/div[2]/div[1]/div/div/select')
    Select(sex_two).select_by_value(sex)

    # 姓氏
    xing_ = u'JING'
    name_ = u'JING'
    driver.find_elements_by_class_name(u'form-control')[3].send_keys(xing_)
    driver.find_elements_by_class_name(u'form-control')[2].send_keys(name_)

    # 国码
    req_country = u'CN'
    req_country_select = driver.find_element_by_xpath(
        u'//*[@id="root"]/div/div[2]/div/div[3]/div[2]/div[1]/div/div/div[1]'
        u'/div/div[2]/div/div[3]/div[1]/div/div/select')
    Select(req_country_select).select_by_value(req_country)
    # tel
    driver.find_elements_by_class_name(u'form-control')[7].send_keys(link_phone)
    # email
    driver.find_elements_by_class_name(u'form-control')[8].send_keys(link_email)
    driver.find_elements_by_class_name(u'form-control')[9].send_keys(link_email)

    # card type
    # card_type = u'mastercard'
    # card_type_element = driver.find_element_by_xpath(
    #     u'//*[@id="card"]/div/div[1]/div/div[2]/div/div[3]/div/div/select')
    # Select(card_type).select_by_value(card_type)
    # 输入卡号

    # creditCardInfo = req.creditCardInfo
    # name = creditCardInfo["name"]
    #
    # cardNumber = creditCardInfo["cardNumber"]
    # driver.find_elements_by_class_name(u'form-control')[12].send_keys(cardNumber)
    # # 持卡人姓名
    # driver.find_elements_by_class_name(u'form-control')[9].send_keys(name)
    # 到期 日
    # validityPeriod = creditCardInfo["validityPeriod"]
    # date = validityPeriod.split("/")
    # end_month = date[0]
    # driver.find_element_by_xpath(
    #     u'//*[@id="card"]/div/div[1]/div/div[2]/div/div[4]/div[3]/div/div[1]/div/select')
    # Select(end_month).select_by_value(end_month)
    # # 到期 年
    # end_year = date[1]
    # driver.find_element_by_xpath(
    #     u'//*[@id="card"]/div/div[1]/div/div[2]/div/div[4]/div[3]/div/div[2]/div/select')
    # Select(end_year).select_by_value(end_year)
    # # cvv/cvc2
    # cvv = creditCardInfo["cvv"]
    # driver.find_elements_by_class_name(u'form-control')[18].send_keys(cvv)
    # # 确认信息
    # driver.find_element_by_id(u'payment-terms').click()
