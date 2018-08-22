# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("window-size=3840,2160")
    # chrome_options.set_headless()
    # # 如果是IT则加上代理
    # if booker_req.ipcc == "IT_F":
    #     chrome_options.add_extension(
    #         get_chrome_proxy_extension(booker_config.get('proxy1', 'dynamicProxy')))
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    d = webdriver.Chrome("/opt/google/chrome/chromedriver", chrome_options=chrome_options)
    d.get("https://agenthub.jetstar.com/TradeLoginAgent.aspx")

    d.find_element_by_id('ControlGroupNewTradeLoginAgentView_AgentNewTradeLoginView_TextBoxUserID').send_keys('lcc_f')

    d.find_element_by_id('ControlGroupNewTradeLoginAgentView_AgentNewTradeLoginView_PasswordFieldPassword').send_keys(
        'Aa123456')

    d.find_element_by_id('ControlGroupNewTradeLoginAgentView_AgentNewTradeLoginView_ButtonLogIn').click();

    element = WebDriverWait(d, 50).until(
        EC.visibility_of_element_located(
            (By.XPATH, '/html/body/div[3]/form/div[7]/div/div/div[2]/div[2]/fieldset[1]/div[1]/div[1]/div[1]/div'))
    )

    time.sleep(3)

    # 单程
    d.find_element_by_id('ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_OneWay').click()

    js = '$("#ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_TextBoxMarketOrigin1").attr("data-airport-code","ADL");' \
         '$("#ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_TextBoxMarketDestination1").attr("data-airport-code","BNE");' \
         '$("#ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_TextboxDepartureDate1").val("16/09/2018");'

    d.find_element_by_id(
        'ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_TextBoxMarketOrigin1').clear()
    d.find_element_by_id(
        'ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_TextBoxMarketOrigin1').send_keys(
        'Adelaide (ADL)')
    d.find_element_by_id(
        'ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_TextBoxMarketDestination1').clear()
    d.find_element_by_id(
        'ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_TextBoxMarketDestination1').send_keys(
        'Cairns (CNS)')

    d.execute_script(js)

    # 查询
    d.find_element_by_id(
        'ControlGroupTradeSalesHomeView_AvailabilitySearchInputTradeSalesHomeView_ButtonSubmit').click()

    # 确认航班
    flight_items = d.find_elements_by_class_name('flight-card-details-price')
    for flight_item in flight_items:
        if flight_item.find_element_by_class_name('flight-code__item').text == 'JQ783':
            flight_item.find_element_by_class_name('price-select__button').click()
            break
    d.find_element_by_id('submit_button').click()

    element = WebDriverWait(d, 50).until(
        EC.visibility_of_element_located(
            (By.ID, 'marketFareKeysDiv'))
    )
    time.sleep(2)
    d.find_element_by_id('submit_button').click()

    element = WebDriverWait(d, 50).until(
        EC.visibility_of_element_located(
            (By.ID, 'all-pax-baggage__radio--ADL-BNE0'))
    )
    d.find_element_by_id('all-pax-baggage__radio--ADL-BNE0').click()
    d.find_element_by_id('submit_button').click()

    # 不选座位
    element = WebDriverWait(d, 50).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, 'js-no-seat-button'))
    )
    d.find_element_by_class_name('js-no-seat-button').click()
    time.sleep(2)
    d.find_element_by_id('submit_button').click()

    # 额外的啥也不选
    element = WebDriverWait(d, 50).until(
        EC.visibility_of_element_located(
            (By.ID, 'hotel-modal'))
    )
    d.find_element_by_id('submit_button').click()

    # 乘客信息

    d.find_element_by_id('passenger_title_0').send_keys('Mr')

    d.find_element_by_id('passenger_Firstname_0').send_keys('dong')

    d.find_element_by_id('passenger_Lastname_0').send_keys('zekun')

    # 联系人信息

    d.find_element_by_id('js-contact_Name_First').send_keys('WANRONG')

    d.find_element_by_id('js-contact_Name_Last').send_keys('WANG')

    d.find_element_by_id('contact_Email_Address').send_keys('lianfenghangbian@163.com')

    d.find_element_by_id('contact_Agent_Email_Address').clear()
    d.find_element_by_id('contact_Agent_Email_Address').send_keys('lianfenghangbian@163.com')

    d.find_element_by_id('contact_Phone_Number').send_keys('18996166498')

    d.find_element_by_id('submit_button').click()

