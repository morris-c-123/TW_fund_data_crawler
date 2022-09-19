"""crawl Taiwan historical fund performance from SITCA"""
import os
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup


def sitca_org_crawler(start, end):
    """input sample value: start=202001, end=202112"""

    # build full range dict

    data_time_dic = {}
    selected_month = datetime(2000, 7, 1)

    for i in range(1, 350):
        output = selected_month.strftime("%Y%m")
        data_time_dic[i] = output
        selected_month = selected_month + relativedelta(months=+1)

    # set duration

    try:
        duration = {
            k: v for k, v in data_time_dic.items() if int(start) <= int(v) <= int(end)}
        # reverse dic
        duration = dict(reversed(duration.items()))

    except:  # pylint: disable = bare-except
        print("Please check the variables of start and end")
    else:
        if not duration:
            print("Please check the variables of start and end")
        else:
            print(f"duration: {duration}")

    # start main code of crawler

    for data_time_number, data_time_str in duration.items():

        # open web

        browser = webdriver.Chrome("./chromedriver")
        browser.get(
            "https://www.sitca.org.tw/ROC/Industry/IN2201.aspx?pid=IN2221_01")

        print("web opened")
        delay_secs = 3
        time.sleep(delay_secs)

        # setting filter

        filter_id = "ctl00_ContentPlaceHolder1_ddlQ_YM"
        year_month = browser.find_element("id", filter_id)
        year_month.click()
        time.sleep(delay_secs)

        # select data time

        month_filter_xpath = "option:nth-child(" + str(data_time_number) + ")"
        month = browser.find_element(By.CSS_SELECTOR, month_filter_xpath)
        month.click()
        time.sleep(delay_secs)

        # submit

        submit = "ctl00_ContentPlaceHolder1_BtnQuery"
        submit = browser.find_element("id", submit)
        submit.click()
        time.sleep(delay_secs)

        print("target page found.")

        # create folder

        output_folder_path = "./data"
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
            print("The new directory is created!")

        file_path = "./data/" + data_time_str + ".csv"

        # create soup

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        title_columns = soup.find_all("td", class_="DTHeader")
        fund_values = soup.find_all("td", {"class": ["DTodd", "DTeven"]})

        # open csv file

        with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            print("csv open")

            # write title columns

            title_list = []

            for i in title_columns:
                title_list.append(i.text)

            print("title columns:" + str(title_list))
            writer.writerow(title_list)

            # 檢查 columns 是否對應 title columns
            if not len(fund_values) % len(title_list) == 0:
                print(
                    "total number of crawled data cannot match the number of title columns")

            # values writerow

            temp_list = []
            for k, v in enumerate(fund_values):
                if not (k+1) % len(title_list) == 0:
                    temp_list.append(v.text)
                else:
                    temp_list.append(v.text)
                    writer.writerow(temp_list)
                    temp_list = []

        browser.quit()
        print("csv file: " + data_time_str + ".csv is created")


sitca_org_crawler(start=200007, end=200811)


def fund_cost_crawler():
    """crawl the latest fund cost"""

    # open web

    browser = webdriver.Chrome("./chromedriver")
    browser.get(
        "https://www.sitca.org.tw/ROC/Industry/IN2211.aspx?pid=IN2222_01")

    print("web opened")
    time.sleep(3)

    # submit

    submit = "ctl00_ContentPlaceHolder1_BtnQuery"
    submit = browser.find_element("id", submit)
    submit.click()
    time.sleep(5)

    print("target page found.")

    # create soup

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # define fund_value_locations

    fund_values = soup.find_all("td", {"class": ["DTodd", "DTeven"]})

    # search fund cost version

    fund_cost_data_version = soup.find_all(
        "option", {"selected": "selected"}, limit=2)
    fund_cost_data_version = "".join([i.text for i in fund_cost_data_version])
    fund_cost_data_version = fund_cost_data_version.replace(" ", "")

    print(f"Data updated version: {fund_cost_data_version}")

    # open csv file

    file_path = "./Fund Cost(" + fund_cost_data_version + ").csv"

    with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        print("csv open")

        # write title columns

        title_list = ["類型代號", "基金統編", "基金名稱",
                      "交易直接成本(A=a1+a2-a3)手續費(a1)金額", "交易直接成本(A=a1+a2-a3)2手續費(a1)比率",
                      "交易直接成本(A=a1+a2-a3)3交易稅(a2)金額", "交易直接成本(A=a1+a2-a3)4交易稅(a2)比率",
                      "交易直接成本(A=a1+a2-a3)5股票ETF及指數型基金申購/買回交易費(a3)金額",
                      "交易直接成本(A=a1+a2-a3)6股票ETF及指數型基金申購/買回交易費(a3)比率",
                      "會計帳列之費用(B=b1+b2+b3+b4)經理費(b1)金額", "會計帳列之費用(B=b1+b2+b3+b4)7經理費(b1)比率",
                      "會計帳列之費用(B=b1+b2+b3+b4)8保管費(b2)金額", "會計帳列之費用(B=b1+b2+b3+b4)9保管費(b2)比率",
                      "會計帳列之費用(B=b1+b2+b3+b4)10保證費(b3)金額", "會計帳列之費用(B=b1+b2+b3+b4)11保證費(b3)比率",
                      "會計帳列之費用(B=b1+b2+b3+b4)12其他項費用(b4)金額", "會計帳列之費用(B=b1+b2+b3+b4)13其他項費用(b4)比率",
                      "合計(=A+B)金額", "合計(=A+B)14比率"]
        print("headers were created")
        writer.writerow(title_list)

        # 檢查 columns 是否對應 title columns
        print("checking number of column")

        if not len(fund_values) % len(title_list) == 0:
            print(
                "total number of crawled data cannot match the number of title columns")

        # values writerow

        print("writing csv")

        temp_list = []
        for k, v in enumerate(fund_values):
            if not (k+1) % len(title_list) == 0:
                temp_list.append(v.text)
            else:
                temp_list.append(v.text)
                writer.writerow(temp_list)
                temp_list = []

    browser.quit()
    print("Finished")


fund_cost_crawler()


def fund_performance_crawler():
    """crawl the latest fund cost"""

    # open web

    browser = webdriver.Chrome("./chromedriver")
    browser.get(
        "https://www.sitca.org.tw/ROC/Industry/IN2307.aspx?pid=IN2232_02")

    print("web opened")
    time.sleep(3)

    # select fund type AA1

    filter_xpath_AA1 = "//select[@id='ctl00_ContentPlaceHolder1_ddlQ_Class']/option[1]"
    month = browser.find_element(By.XPATH, filter_xpath_AA1)
    month.click()
    time.sleep(3)

    # submit

    submit = "ctl00_ContentPlaceHolder1_BtnQuery"
    submit = browser.find_element("id", submit)
    submit.click()
    time.sleep(5)

    print("AA1 page found.")

    # create soup AA1

    soupAA1 = BeautifulSoup(browser.page_source, 'html.parser')

    # select fund type AA2

    filter_xpath_AA2 = "//select[@id='ctl00_ContentPlaceHolder1_ddlQ_Class']/option[2]"
    month = browser.find_element(By.XPATH, filter_xpath_AA2)
    month.click()
    time.sleep(3)

    # submit

    submit = "ctl00_ContentPlaceHolder1_BtnQuery"
    submit = browser.find_element("id", submit)
    submit.click()
    time.sleep(5)

    print("AA2 page found.")

    # create soup AA2

    soupAA2 = BeautifulSoup(browser.page_source, 'html.parser')

    # define fund_value_locations

    fund_values_AA1 = soupAA1.find_all(
        "td", {"class": ["DTodd", "DTeven", "DTsubtotal"]})
    fund_values_AA2 = soupAA2.find_all(
        "td", {"class": ["DTodd", "DTeven", "DTsubtotal"]})

    # search fund cost version

    fund_cost_data_version = soupAA1.find(
        "option", {"selected": "selected"})
    fund_cost_data_version = fund_cost_data_version.text
    fund_cost_data_version = fund_cost_data_version.replace(" ", "")

    print(f"Data updated version: {fund_cost_data_version}")

    # open csv file

    file_path = "./Fund Performance(" + fund_cost_data_version + ").csv"

    with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        print("csv open")

        # write title columns

        title_list = ["基金類型(註1)", "基金名稱", "公司名稱", "6個月-報酬率%",
                      "6個月-報酬率排名", "6個月-週轉率%", "6個月-週轉率排名",
                      "1年-報酬率%", "1年-報酬率排名", "1年-週轉率%", "1年-週轉率排名",
                      "3年-報酬率%", "3年-報酬率排名", "3年-週轉率%", "3年-週轉率排名",
                      "5年-報酬率%", "5年-報酬率排名", "5年-週轉率%", "5年-週轉率排名"]

        print("headers were created")
        writer.writerow(title_list)

        # 檢查 columns 是否對應 title columns
        print("checking number of column")

        for fund_values in [fund_values_AA1, fund_values_AA2]:

            if not len(fund_values) % len(title_list) == 0:
                print(
                    "total number of data columns cannot match the number of title columns")

            # values writerow

            print("writing csv")

            temp_list = []
            for k, v in enumerate(fund_values):
                if not (k+1) % len(title_list) == 0:
                    temp_list.append(v.text)
                else:
                    temp_list.append(v.text)
                    location_of_adding_percentage = [
                        3, 5, 7, 9, 11, 13, 15, 17]
                    for add in location_of_adding_percentage:
                        temp_list[add] = temp_list[add].replace(" ", "")+"%"
                    writer.writerow(temp_list)
                    temp_list = []

    browser.quit()
    print("Finished")


fund_performance_crawler()


def TAIEX_crawler_5_year():
    """crawl 5 year data of TAIEX since this month"""

    # open web

    browser = webdriver.Chrome("./chromedriver")
    browser.get(
        "https://www.twse.com.tw/zh/page/trading/indices/MI_5MINS_HIST.html")

    print("web opened")
    time.sleep(3)

    # open csv file

    today = datetime.today().date()
    file_path = "./TAIEX index(" + str(today) + ").csv"

    with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        print("csv open")
        headers_were_created = False

        # set five year duration filter (create filter_list)

        month = datetime.today().month
        year = 1
        filter_list = []

        for i in range(60):
            if not month == 1:
                filter_list.append([str(year), str(month)])
                month -= 1
            else:
                filter_list.append([str(year), str(month)])
                year += 1
                month = 12

        # select filter

        for yy, mm in filter_list:
            year = browser.find_element(
                By.XPATH, "//select[@name='yy']/option[" + yy + "]")
            month = browser.find_element(
                By.XPATH, "//select[@name='mm']/option[" + mm + "]")
            submit = browser.find_element(By.PARTIAL_LINK_TEXT, "查詢")
            year.click()
            month.click()
            submit.click()
            time.sleep(3)

            # create soup

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            print("crawling data of" + yy + "/" + mm)
            # define fund_value_locations

            headers = soup.find_all(
                "th", {"class": "dt-head-center dt-body-center sorting"})
            index_value = soup.find_all(
                "td", {"class": "dt-head-center dt-body-center"})

            # write headers

            if headers_were_created is False:
                title_list = []

                for i in headers:
                    title_list.append(i.text)
                writer.writerow(title_list)
                headers_were_created = True
                print("headers:" + str(title_list))

                # 檢查 columns 是否對應 title columns
                if not len(index_value) % len(title_list) == 0:
                    print(
                        "total number of index_value cannot match the number of headers")

            # values writerow

            temp_list = []
            for k, v in enumerate(index_value):
                if not (k+1) % len(title_list) == 0:
                    temp_list.append(v.text)
                else:
                    temp_list.append(v.text)
                    writer.writerow(temp_list)
                    temp_list = []

    browser.quit()
    print("""Finished!!
csv file: TAIEX index(" + str(today) + ").csv is created""")


TAIEX_crawler_5_year()
