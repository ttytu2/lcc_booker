# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from data_message import DataMessage
from conf import booker_config
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CreateOrderProcess(object):

    @staticmethod
    def confirm_flightNumber(browser, req):
        # 点击含税报价
        element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "haveShui")))
        element.click()

        # 判断航班号
        element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "btn-book"))
        )
        flight_items = browser.find_element_by_class_name("goway").find_elements_by_class_name("flight-item-new")
        for flight_item in flight_items:
            flightNumber = flight_item.find_element_by_class_name("f-c-name").text.split(" ")[1]
            if req.fromSegments[0]["flightNumber"] in flightNumber:
                flight_item.find_element_by_class_name("btn-book").click()
                break

        # 获取预订最低价（官网专享）
        element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "cabin-item-new"))
        )
        time.sleep(1)
        cabin_items = browser.find_elements_by_class_name("cabin-item-new")

        for index, item in enumerate(cabin_items):

            # 查找最低价
            price = int(
                item.find_element_by_class_name("currency").find_element_by_tag_name("em").get_attribute(
                    'textContent'))
            if int(req.adultNumber) > 0 and price <= req.adultPrice + req.adultTax + booker_config.getint("carrier9C", "jumpPrice"):
                book = item.find_element_by_class_name("btn-c-book")
                action = webdriver.ActionChains(browser)
                action.move_to_element(book)
                action.click(book)
                action.perform()
                break
            if int(req.childNumber) > 0 and price <= req.childPrice + req.childTax + booker_config.getint("carrier9C", "jumpPrice"):
                book = item.find_element_by_class_name("btn-c-book")
                action = webdriver.ActionChains(browser)
                action.move_to_element(book)
                action.click(book)
                action.perform()
                break
            if index == len(cabin_items) - 1:
                raise Exception("Not Founf Right Price For This Flight")

        if req.flightOption == 2:
            time.sleep(4)
            flight_items = browser.find_element_by_class_name("retway").find_elements_by_class_name("flight-item-new")
            for flight_item in flight_items:
                flightNumber = flight_item.find_element_by_class_name("f-c-name").text.split(" ")[1]
                if req.retSegments[0]["flightNumber"] in flightNumber:
                    flight_item.find_element_by_class_name("btn-book").click()
                    break

            # 获取预订最低价（官网专享）
            time.sleep(4)
            element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "cabin-item-new"))
            )
            cabin_items = browser.find_elements_by_class_name("cabin-item-new")

            for index, item in enumerate(cabin_items):
                if index == len(cabin_items) - 1:
                    item.find_element_by_class_name("btn-c-book").click()
                    break

    @staticmethod
    def fill_in_information(browser, req):

        link_name = booker_config.get('linkManInfo', 'name')
        link_phone = booker_config.get('linkManInfo', 'phone')
        link_email = booker_config.get('linkManInfo', 'email')

        # 填写所有乘客信息
        element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div[1]/ul[3]/li[1]'))
        )  # FamilyName
        passengers = req.passengers
        passenger_items = browser.find_element_by_class_name("m-forms").find_elements_by_class_name(
            "passenger-item")
        for index, passenger in enumerate(passenger_items):
            inputs = passenger.find_elements_by_tag_name('input')
            for input in inputs:
                if input.get_attribute('data-name') == 'FamilyName':
                    input.send_keys(passengers[index]["lastName"])
                if input.get_attribute('data-name') == 'PersonalName':
                    input.send_keys(passengers[index]["firstName"])
                if input.get_attribute('data-name') == 'Mobile':
                    input.send_keys(link_phone)
                if input.get_attribute('data-name') == 'Birthday':
                    input.send_keys(passengers[index]["birthday"])
                if input.get_attribute('data-name') == 'CertificateNo':
                    input.send_keys(passengers[index]["cardNum"])
                if input.get_attribute('data-name') == 'CertificateExpireDate':
                    input.send_keys(passengers[index]["cardExpired"])

            drops = passenger.find_elements_by_class_name("c-drop")
            for i, drop in enumerate(drops):
                drop.click()
                if i == 0:
                    select_items = drop.find_elements_by_class_name("u-select-item")

                    if passengers[index]["cardType"] == 'PP':
                        for select_item in select_items:
                            if select_item.get_attribute('data-value') == '2':
                                select_item.click()
                    if passengers[index]["cardType"] == 'TB':
                        for select_item in select_items:
                            if select_item.get_attribute('data-value') == '3':
                                select_item.click()
                    if passengers[index]["cardType"] == 'HX':
                        for select_item in select_items:
                            if select_item.get_attribute('data-value') == '10':
                                select_item.click()
                    if passengers[index]["cardType"] == 'GA':
                        for select_item in select_items:
                            if select_item.get_attribute('data-value') == '13':
                                select_item.click()
                    if passengers[index]["cardType"] == 'TW':
                        for select_item in select_items:
                            if select_item.get_attribute('data-value') == '19':
                                select_item.click()

                if i == 1:
                    select_items = drop.find_elements_by_class_name("u-select-item")
                    for select in select_items:
                        if select.get_attribute('data-value') == DataMessage.get_change_country_code(
                                passengers[index]["cardIssuePlace"]):
                            select.click()
                if i == 2:
                    select_items = drop.find_elements_by_class_name("u-select-item")
                    for select in select_items:
                        if select.get_attribute('data-value') == DataMessage.get_change_country_code(
                                passengers[index]["nationality"]):
                            select.click()
                if i == 3:
                    select_items = drop.find_elements_by_class_name("u-select-item")
                    if passengers[index]["gender"] == 'M':
                        select_items[0].click()
                    else:
                        select_items[1].click()
        link_inputs = browser.find_element_by_class_name("c-link").find_element_by_class_name(
            "passenger-item").find_elements_by_tag_name('input')

        for index, link_input in enumerate(link_inputs):
            if index == 0:
                link_input.clear()
                link_input.send_keys(link_name)
            if index == 2:
                link_input.clear()
                link_input.send_keys(link_phone)
            if index == 3:
                link_input.clear()
                link_input.send_keys(link_email)

        time.sleep(2)
        browser.find_element_by_class_name("J_checkbox").click()
        browser.find_element_by_class_name("order-next").click()

    @staticmethod
    def confirmation_information(browser, req):
        # 所有增值业务设置为不选取
        element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'shopping-seg'))
        )
        shopping_segs = browser.find_elements_by_class_name("passenger-item")
        for shopping in shopping_segs:
            shopping.click()
            option_items = shopping.find_elements_by_class_name("option-item")
            for index, option in enumerate(option_items):
                if index == len(option_items) - 1:
                    option.click()
        browser.find_element_by_class_name("btn-submit").click()
        time.sleep(2)

        browser.find_element_by_xpath("/html/body/div[2]/div[6]/div/div[1]/a[2]").click()
        browser.find_element_by_css_selector("button.modal-btn:nth-child(1)").click()

        #
        # J_Nexts = browser.find_element_by_xpath("/html/body/div[2]/div[6]/div/div[1]/a[2]").click()
        # action = webdriver.ActionChains(browser)
        # action.move_to_element(J_Nexts[1])
        # action.perform()
        # for index, j_next in enumerate(J_Nexts):
        #     if index == 1:
        #         j_next.click()
        #         btn_cancel = browser.find_element_by_class_name("btn-cancel")
        #         action = webdriver.ActionChains(browser)
        #         action.move_to_element(btn_cancel)
        #         action.click(btn_cancel)
        #         action.perform()
        #         break

        # 确认乘客信息 订单确认
        # element = WebDriverWait(browser, booker_config.getint('carrier9C', 'waitTimeout')).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'agreecheck'))
        # )
        # browser.find_element_by_class_name("agreecheck").click()
        # browser.find_element_by_class_name("J-next").click()
