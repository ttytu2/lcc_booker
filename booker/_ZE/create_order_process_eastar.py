# -*- coding: utf-8 -*-
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conf import booker_config


class CreateOrderProcess(object):
    @staticmethod
    def confirm_flightNumber(browser, req):
        WebDriverWait(browser, 100).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "air_goods_list"))
        )
        start_air_list = browser.find_elements_by_class_name("air_goods_list")[0].find_element_by_tag_name(
            "tbody").find_elements_by_tag_name("tr")
        snumber = req.fromSegments[0]["flightNumber"]
        air_price(browser, start_air_list, snumber)
        # 返航
        if req.flightOption == 2:
            return_air_list = browser.find_elements_by_class_name("air_goods_list")[1].find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr")
            rnumber = req.retSegments[0]["flightNumber"]
            air_price(browser, return_air_list, rnumber)

    @staticmethod
    def fill_in_information(browser, req):
        WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.ID, "reserver_last_name")))
        # 同意协议
        all_agree = browser.find_element_by_id("PNWBA00013").find_element_by_id('divTerms').\
            find_elements_by_class_name("term")
        all_agree_list = []
        t = booker_config.getint('eastarjet', 'time')
        time.sleep(t)
        for agree_option in all_agree:
            all_agree_list.append(agree_option)
            agree_option.find_elements_by_class_name('iradio_minimal-red')[0].click()
        # 下滑到一半
        js = "var q=document.documentElement.scrollTop=800;$('.r_birth').find('input').attr('type','text')"
        browser.execute_script(js)
        browser.find_elements_by_class_name("tel")[1].find_element_by_class_name("icheckbox_minimal-red").click()
        # 乘客信息填写
        passengers = browser.find_element_by_class_name("grouping").find_elements_by_tag_name("tbody")
        i = 0
        a = 0
        for index, passenger in enumerate(passengers):
            if index % 2 == 0:
                if req.passengers[i]["gender"] == "F":
                    passenger.find_element_by_class_name("gender").find_elements_by_tag_name("li")[
                        1].find_element_by_class_name("iradio_minimal-red").click()
                elif req.passengers[i]["gender"] == "M":
                    passenger.find_element_by_class_name("gender").find_elements_by_tag_name("li")[
                        0].find_element_by_class_name("iradio_minimal-red").click()
                passenger.find_element_by_name("last_name").send_keys(req.passengers[i]["lastName"])
                passenger.find_element_by_name("first_name").send_keys(req.passengers[i]["firstName"])
                birthday = req.passengers[i]["birthday"].split("-")
                year = birthday[0]
                month = birthday[1]
                day = birthday[2]
                brd = passenger.find_element_by_class_name("r_birth").find_elements_by_tag_name("input")
                brd[0].send_keys(year)
                brd[1].send_keys(month)
                brd[2].send_keys(day)
                i += 1
        # 追加信息
                # 护照国家
            if index % 2 == 1:
                if len(all_agree_list) > 2:
                    passenger.find_element_by_class_name('c1').find_element_by_class_name("selectBox").click()
                    nationlity = passenger.find_element_by_class_name('c1').find_elements_by_tag_name("a")
                    for item in nationlity:
                        if req.passengers[a]["nationality"] == item.get_attribute("data-value"):
                            item.click()
                            break
                    # 护照信息
                    passenger.find_element_by_name('passport_num').send_keys(req.passengers[a]["cardNum"])
                    # 护照到期时间
                    card_ex = req.passengers[a]["cardExpired"].split("-")
                    card_ex_year = card_ex[0]
                    card_ex_month = card_ex[1]
                    card_ex_day = card_ex[2]
                    passenger.find_element_by_class_name("p_birth").find_elements_by_class_name("selectBox")[0].click()
                    passport_year = passenger.find_element_by_class_name('passport_year').find_elements_by_tag_name('a')
                    for item in passport_year:
                        if card_ex_year == item.text:
                            item.click()
                            break
                    passenger.find_element_by_class_name("p_birth").find_elements_by_class_name("selectBox")[1].click()
                    passport_month = passenger.find_element_by_class_name('passport_month').find_elements_by_tag_name('a')
                    for item in passport_month:
                        if card_ex_month == item.text:
                            item.click()
                            break
                    passenger.find_element_by_class_name("p_birth").find_elements_by_class_name("selectBox")[2].click()
                    passport_day = passenger.find_element_by_class_name('passport_day').find_elements_by_tag_name('a')
                    for item in passport_day:
                        if card_ex_day == item.text:
                            item.click()
                            break
                    # 发行护照国家
                    passenger.find_element_by_class_name('c2').find_element_by_class_name("selectBox").click()
                    all_issueplace = passenger.find_element_by_class_name('c2').find_elements_by_tag_name("a")
                    for item in all_issueplace:
                        if req.passengers[a]["cardIssuePlace"] == item.get_attribute("data-value"):
                            item.click()
                            break
                    a += 1
                else:
                    id_discount = passenger.find_element_by_class_name('identity').\
                        find_element_by_class_name("selectBox")
                    id_discount.click()
                    id_discount.find_elements_by_tag_name("li")[0].find_element_by_tag_name("a").click()

        # 确定
        p = booker_config.getint('eastarjet', 'passenger_time')
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
        time.sleep(3)
        browser.find_element_by_id("PNWBA00013").find_element_by_class_name('btn-color04').click()
        time.sleep(p)
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
        time.sleep(3)
        browser.find_element_by_id('PNWBA00033').find_element_by_class_name('btn-color04').click()
        time.sleep(2)

    @staticmethod
    def creditcard_payment(browser, req):
        """
        支付页面有两种形式，此为输入信用卡号的形式（无航空指南）
        :param browser:
        :param req:东京到首尔，
        :return:
        """
        WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.ID, 'foreign_credit_card')))
        browser.find_element_by_id("foreign_credit_card").find_element_by_class_name("iradio_minimal-red").click()
        creditInfo = req.creditCardInfo
        cardNumber = creditInfo["cardNumber"]
        cutCardNum = cardNumber.split(" ")
        name = creditInfo["name"]
        firstName = name.split(" ")[0]
        lastName = name.split(" ")[1]
        browser.find_element_by_id('jpy_card_1').send_keys(cutCardNum[0])
        browser.find_element_by_id("jpy_card_2").send_keys(cutCardNum[1])
        browser.find_element_by_id("jpy_card_3").send_keys(cutCardNum[2])
        browser.find_element_by_id("jpy_card_4").send_keys(cutCardNum[3])
        card_expire = creditInfo["validityPeriod"]
        card_expire_Num = card_expire.split("/")
        browser.find_element_by_id("jpy_mm").send_keys(card_expire_Num[0])
        browser.find_element_by_id("jpy_yy").send_keys(card_expire_Num[1])
        browser.find_element_by_id("jpy_cvc").send_keys(creditInfo["cvv"])
        # 下滑到底部
        js = "var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        ch = browser.current_window_handle
        browser.find_element_by_id("PNWBA00014").find_element_by_class_name("icheckbox_minimal-red").click()
        browser.find_element_by_id("PNWBA00014").find_element_by_class_name("btn-color04").click()
        t = booker_config.getint('eastarjet', 'time')
        time.sleep(t)
        # 所有的window handles
        wh = browser.window_handles
        # 在所有窗口中查找弹出窗口
        browser.switch_to.window(wh[-1])
        time.sleep(t)
        cardNumber = creditInfo["cardNumber"]
        cutCardNum = cardNumber.split(" ")
        browser.find_element_by_id("viewcardno1").send_keys(cutCardNum[0])
        browser.find_element_by_id("viewcardno2").send_keys(cutCardNum[1])
        browser.find_element_by_id("viewcardno3").send_keys(cutCardNum[2])
        browser.find_element_by_id("viewcardno4").send_keys(cutCardNum[3])
        cvv = creditInfo["cvv"]
        browser.find_element_by_name("cvv").send_keys(cvv)
        validityPeriod = creditInfo["validityPeriod"]
        date = validityPeriod.split("/")
        # 下拉按钮：月份，年份
        browser.find_element_by_id("monthtd").click()
        a = browser.find_element_by_id("monthtd").find_element_by_class_name("sbOptions")
        time.sleep(t)
        a.find_elements_by_tag_name("li")[int(date[0])].find_element_by_tag_name("a").click()
        browser.find_element_by_id("yeartd").click()
        time.sleep(t)
        YY = browser.find_element_by_id("yeartd").find_element_by_class_name("sbOptions").find_elements_by_tag_name(
            "li")
        for item in YY:
            YY_value = item.find_element_by_tag_name("a").text
            if date[1] in YY_value:
                item.click()
                break
        # 名字
        browser.find_element_by_id("fname").send_keys(firstName)
        browser.find_element_by_id("lname").send_keys(lastName)
        browser.find_element_by_class_name("footer_btn").click()
        time.sleep(2)
        browser.find_element_by_id("JPY").click()
        browser.find_element_by_name("agree").click()
        browser.find_element_by_class_name("btn-primary").click()

    @staticmethod
    def creditcard_payment_two(browser, req):
        """
        支付页面有两种形式，此为输入名字和email的形式
        有航空指南的一定是跨国，必填追加信息.支付页面是填email.
        无航空指南的韩国国内行程乘客信息无追加信息仅有折扣一栏.会弹出信用卡窗口，支付页面选择国外卡，填email.
        :param browser:
        :param req:
        :return:
        """
        WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.ID, 'foreign_credit_card')))
        browser.find_element_by_id("foreign_credit_card").find_element_by_class_name("iradio_minimal-red").click()
        creditCardInfo = req.creditCardInfo
        name = creditCardInfo["name"]
        firstName = name.split(" ")[0]
        lastName = name.split(" ")[1]
        linkEmail = booker_config.get('linkManInfo', 'email')
        browser.find_element_by_id("krp_last_name").send_keys(lastName)
        browser.find_element_by_id("krp_first_name").send_keys(firstName)
        browser.find_element_by_id("krp_email").send_keys(linkEmail)
        # 下滑到底部
        js = "var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        ch = browser.current_window_handle
        browser.find_element_by_id("PNWBA00014").find_element_by_class_name("icheckbox_minimal-red").click()
        browser.find_element_by_id("PNWBA00014").find_element_by_class_name("btn-color04").click()
        t = booker_config.getint('eastarjet', 'time')
        time.sleep(t)
        # 所有的window handles
        wh = browser.window_handles
        # 在所有窗口中查找弹出窗口
        browser.switch_to.window(wh[-1])
        time.sleep(t)
        cardNumber = creditCardInfo["cardNumber"]
        cutCardNum = cardNumber.split(" ")
        browser.find_element_by_id("viewcardno1").send_keys(cutCardNum[0])
        browser.find_element_by_id("viewcardno2").send_keys(cutCardNum[1])
        browser.find_element_by_id("viewcardno3").send_keys(cutCardNum[2])
        browser.find_element_by_id("viewcardno4").send_keys(cutCardNum[3])
        cvv = creditCardInfo["cvv"]
        browser.find_element_by_name("cvv").send_keys(cvv)
        validityPeriod = creditCardInfo["validityPeriod"]
        date = validityPeriod.split("/")
        # 下拉按钮：月份，年份
        browser.find_element_by_id("monthtd").click()
        a = browser.find_element_by_id("monthtd").find_element_by_class_name("sbOptions")
        time.sleep(t)
        a.find_elements_by_tag_name("li")[int(date[0])].find_element_by_tag_name("a").click()
        browser.find_element_by_id("yeartd").click()
        time.sleep(t)
        YY = browser.find_element_by_id("yeartd").find_element_by_class_name("sbOptions").find_elements_by_tag_name("li")
        for item in YY:
            YY_value = item.find_element_by_tag_name("a").text
            if date[1] in YY_value:
                item.click()
                break
        # 名字
        browser.find_element_by_id("fname").send_keys(firstName)
        browser.find_element_by_id("lname").send_keys(lastName)
        browser.find_element_by_class_name("footer_btn").click()
        time.sleep(2)

        # 注：多次验证发现情形不同的情况下，想选择的按钮id，class有变，故而用以下形式
        bizhong = browser.find_element_by_id("confirmText").find_elements_by_tag_name("label")
        for item in bizhong:
            bizhong_type = item.text[0]
            if bizhong_type == "GBP":  # 有可能无此项
                continue
            item.click()

        browser.find_element_by_name("agree").click()
        browser.find_element_by_class_name("btn-primary").click()

    @staticmethod
    def creditcard_payment_no_guide(browser, req):
        flag = judge_msgBox(browser)
        if flag is True:  # 有提示框
            browser.find_element_by_id('msgBox').find_element_by_id('alertBox'). \
                find_element_by_class_name('btn-color04').click()
            CreateOrderProcess.creditcard_payment_two(browser, req)
        else:  # 无提示框是去日本的行程
            CreateOrderProcess.creditcard_payment(browser, req)


def judge_msgBox(browser):
    try:
        browser.find_element_by_id('msgBox').find_element_by_id('alertBox').\
            find_element_by_class_name('btn-color04')
        return True
    except:
        return False


def air_price(browser, air_list, number):
    """
    对应航线选择最便宜的价格
    :param air_list:
    :param number:
    :return:
    """
    price_line = []
    for air in air_list:  # tr
        if air.get_attribute("flightnumbertext") == number:
            price_line.append(air)  # 获取对应航班的那一行
            break
    all_price = []
    price_list = price_line[0].find_elements_by_class_name('opt_upgrade')  # 找到所有有效的价格
    price_button_list = []
    # 获取最低价格
    for price_button in price_list:
        price_input = price_button.find_element_by_tag_name('label').text  # 获取价格标签
        price_split = price_input.split(' ')  # 只获取数值
        str_price = int(str(price_split[0]).replace(",", ''))
        all_price.append(str_price)  # 数值分别加入列表
        price_button_list.append(price_button)  # 相对应的按钮加入列表
    min_price = min(all_price)
    price_index = all_price.index(min_price)  # 找到最小值的位置
    price_button_list[price_index].click()  # 点击相对应的按钮
    t = booker_config.getint('eastarjet', 'time')
    time.sleep(t)
    browser.find_element_by_id("PNWBA00020").find_elements_by_tag_name("a")[1].click()
