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

            # odd columns

            # 檢查 odd columns 是否對應 title columns
            if not len(fund_values) % len(title_list) == 0:
                print(
                    "total number of crawled odd data cannot match the number of title columns")

            # odd values writerow

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

