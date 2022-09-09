"""crawl Taiwan historical fund performance from SITCA"""
import os
import csv
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dateutil.relativedelta import relativedelta


def data_time_dic_generator(start, end):
    """generate {1:'200007', ...}
    input value: start, end
    """
    
    # build full range dict
    
    data_time_dic = {}
    selected_month = date(2000, 7, 1)

    for i in range(1, 300):
        if selected_month.month < 10:
            output = str(str(selected_month.year) +
                         "0" + str(selected_month.month))
        else:
            output = str(str(selected_month.year) + str(selected_month.month))

        data_time_dic[i] = output
        selected_month = selected_month + relativedelta(months=+1)
    
    # select duration
    
    data_duration_to_download = [i for i in range(start, end+1)]
    dict_data_duration_to_download = {
        x: data_time_dic[x] for x in data_duration_to_download}

    print("""dict_name: data_time_dic; details: """)
    print(dict_data_duration_to_download)

    return dict_data_duration_to_download


def sitca_org_crawler(duration):
    """input: duration"""
    for data_time_number, data_time_str in duration.items():

        # open web

        browser = webdriver.Chrome("./chromedriver")
        browser.get(
            "https://www.sitca.org.tw/ROC/Industry/IN2201.aspx?pid=IN2221_01")

        print("web opened")
        delay_secs = 5
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

        print("target found.")

        # scraping as csv

        print("start scraping as csv")
        loop_break = 0

        # create folder

        output_folder_path = "./data"
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
            print("The new directory is created!")

        file_path = "./data/" + data_time_str + ".csv"

        with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            print("csv open")

            for fund in range(1, 10000):
                if loop_break == 1:
                    loop_break = 0
                    print("總計 was found. stop scrawling")
                    break

                temp_list = []

                for column in range(1, 18):
                    locate = '//*[@id="GlobalTable"]/tbody/tr[3]/td/table/tbody/tr[' + \
                        str(fund) + ']/td[' + str(column) + ']'

                    try:
                        fund_data = browser.find_element(By.XPATH, locate)

                    # set not_found element as blank

                    except NoSuchElementException:
                        temp_list.append("")

                    else:
                        if "總計" in str(fund_data.text):
                            loop_break = 1
                            break

                        temp_list.append(fund_data.text)

                writer.writerow(temp_list)

        browser.quit()
        print("csv file: " + data_time_str + ".csv was created")


data_time = data_time_dic_generator(151, 152)
sitca_org_crawler(data_time)

