# -*- coding: utf-8 -*-
import time
import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from create_order_process_eastar import CreateOrderProcess
from conf import booker_config


class EastarJet(object):
    logger = logging.getLogger()

    @staticmethod
    def get_air_list(browser, req):

        browser.get("https://www.eastarjet.com/")
        WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "iradio_minimal-red")))
        # 如果是单程
        if req.flightOption != 2:
            browser.find_element_by_id("PNWHC00001_icheck").find_elements_by_tag_name("li")[1].click()
        # 出发地
        browser.find_element_by_id("PNWHC00001_departure_anchor").click()
        from_citys = browser.find_element_by_id("PNWHC00001_departure_list").find_elements_by_tag_name("a")
        for city in from_citys:
            if req.fromCity == city.get_attribute("data-value"):
                city.click()
                break
        to_citys = browser.find_element_by_id("PNWHC00001_arrival_list").find_elements_by_tag_name("dd")
        for city in to_citys:
            if req.toCity == city.find_element_by_tag_name("a").get_attribute("data-value"):
                city.click()
                break
        # 填写时间(之前的js写法，Firefox浏览器出问题，故换成点击事件)
        stime = req.startTime
        select_time(browser, stime)
        if req.flightOption == 2:
            etime = req.endTime
            select_time(browser, etime)
        time.sleep(2)
        # 选择乘客
        PG_element = browser.find_element_by_class_name('id_perspn').find_element_by_class_name('txt').click()
        if req.adultNumber > 1:
            a = 1
            i = int(req.adultNumber)
            while a < i:
                browser.find_element_by_id('PNWHC00001').find_elements_by_class_name('addPlus')[0].click()
                a += 1
        if req.childNumber > 0:
            a = 0
            i = int(req.childNumber)
            while a < i:
                browser.find_element_by_id('PNWHC00001').find_elements_by_class_name('addPlus')[1].click()
                a += 1
        # 乘客确定
        browser.find_element_by_class_name('person_outer').find_element_by_class_name("btn-color04").click()
        # 查询
        browser.find_elements_by_class_name("form_tbl")[3].find_element_by_tag_name("a").click()

    @staticmethod
    def do_booker_login(browser, req):
        # 下滑到底部
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
        time.sleep(2)
        total_price = browser.find_element_by_class_name("tot_price").text
        req.total_price = total_price
        # 判断如果价格超出要求单价，则停止运行：
        if total_price[0]*req.exchange*0.985 <= req.price:
            browser.quit()
        browser.find_element_by_class_name("mo_type").find_element_by_tag_name("a").click()
        time.sleep(2)
        trans_windows = browser.find_element_by_id("PNWBA00005").find_element_by_class_name("btn-color04")
        if trans_windows.is_displayed():  # 如果跳出航行指南
            req.judge_airline = 1
            trans_windows.click()
        # 如果不是跨国行会报错
        time.sleep(1)
        # 会员登录
        account = booker_config.get('eastarjet', 'account')
        password = booker_config.get('eastarjet', 'password')
        req.username = account
        req.password = password
        if account:
            browser.find_element_by_id("PNWHB00003_userId").send_keys(account)
            browser.find_element_by_id("PNWHB00003_userPw").send_keys(password)
            browser.find_element_by_id("PNWHB00003").find_elements_by_class_name("btn-color04")[0].click()
            time.sleep(3)
            browser.find_element_by_id("msgBox").find_element_by_class_name("btn-color04").click()
        else:  # 非会员预订
            browser.find_element_by_link_text('非会员预订').click()
            time.sleep(2)
            browser.find_element_by_link_text('继续').click()

    def get_booker_result(self, browser, req):
        try:
            # 选择行程类型
            self.get_air_list(browser, req)
            # 判断航班号
            CreateOrderProcess.confirm_flightNumber(browser, req)
        except Exception as e:
            self.logger.error("flightnumber exception: {0}".format(e), exc_info=1)
            result = {"status": "1", "message": "No flight number found"}
            return result
        # 登录
        try:
            self.do_booker_login(browser, req)
            # 填写所有乘客信息
            CreateOrderProcess.fill_in_information(browser, req)
        except Exception as e:
            self.logger.error("passenger exception: {0}".format(e), exc_info=1)
            result = {"status": "2", "message": "Passenger information is wrong"}
            return result
        try:
            # 信用卡付款
            if req.judge_airline == 0:  # 无航空指南
                CreateOrderProcess.creditcard_payment_no_guide(browser, req)
            else:  # 有航空指南
                CreateOrderProcess.creditcard_payment_two(browser, req)
        except Exception as e:
            self.logger.error("payment exception: {0}".format(e), exc_info=1)
            result = {"status": "5", "message": "Payment exception"}
            return result

        result = {"status": "0", "message": "Order successfully created", "orderNumber": req.order_number,
                  "orderPrice": req.total_price, "orderUsername": req.username, "orderPassword": req.password}

        self.logger.debug(result)

        return result


def select_time(browser, time_op):
    """
    选择航线中的时间填写(中文网站)
    :param browser:
    :param time_op:2018-4-3
    :return:
    """
    table_time = browser.find_element_by_class_name("table-condensed")
    table_month = table_time.find_element_by_class_name("datepicker-switch")
    table_month.click()
    # 选择月份
    time_split = time_op.split('-')  # 拆分日期
    date = str(int(time_split[2]))  # 去除0
    month = time_split[1]
    loca_m = int(month) - 1
    browser.find_element_by_class_name("datepicker-months").find_elements_by_tag_name('span')[loca_m].click()
    # 选择日期
    table_day = browser.find_element_by_class_name(" table-condensed").find_elements_by_tag_name('td')
    for day_option in table_day:
        all_day_classname = day_option.get_attribute('class')  # 包括上个月的日期
        if all_day_classname == 'day':  # 选中这个月的所有
            day_value = day_option.text
            if date in day_value:
                day_option.click()
                break