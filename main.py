
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import pandas as pd
import csv
import os.path
import time
import requests
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

url = 'https://www.example.com/'
url2 = 'https://www.example1.com/'
url3 = 'https://www.example2.com/'
url4 = 'https://www.example3.com/'
url5 = 'https://www.example4.com/'


class Test(object):
    def __init__(self):
        # self.options = Options()####
        # self.options.add_argument('--headless')####
        # self.options.add_argument('--disable-gpu')####
        #caps = DesiredCapabilities().CHROME
        #caps["pageLoadStrategy"] = "none"
        self.s = Service('C:\webdriver\chromedriver.exe')
        self.browser = webdriver.Chrome(service=self.s)  ###, options=self.options desired_capabilities=caps,


    def login_proces(self):
        self.browser.get(url)
        self.browser.implicitly_wait(2)

        m = self.browser.find_element("id", 'userID')
        m.send_keys('')#login
        time.sleep(0.1)
        m1 = self.browser.find_element("id", 'password')
        m1.send_keys('')#password
        time.sleep(0.1)
        m1.send_keys(Keys.TAB)
        m1.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(2)
        self.browser.find_element(By.ID, "CybotCookiebotDialogBodyButtonAccept").click()
        self.browser.implicitly_wait(2)

    def microsoft_conf(self):
        time.sleep(2)
        self.browser.get(url2)
        self.browser.implicitly_wait(2)
        self.browser.find_element(By.ID, "idBtn_Back").click()  # id microsoftu
        self.browser.implicitly_wait(7)

    def product(self, id_prod):
        time.sleep(2)
        l = self.browser.find_element("id", 'searchText')
        l.send_keys(id_prod)
        l.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(1)
        try:
            self.browser.find_element(By.ID, "product-code-1").click()
        except:
            # print('nie było wiecej niz jednego')
            pass

        self.browser.implicitly_wait(1)

    def zdjecia(self, id_prod):
        # images
        html_doc = self.browser.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        x = soup.find_all(class_='modal-image')

        # prices
        # id="price-list"
        # id="price-list"
        try:
            kat = soup.find(id="price-list").text
            kat = kat.replace("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t", '')
            net = soup.find(id="net-price").text
            net = net.replace("\n\t\t\t\t\t\t\t\t\t", '')
            # print(id_prod, "^", x, "^", kat, "^", net)####### dodać ceny produktów

            ceny = list()
            ceny.append(id_prod)
            ceny.append("^")
            ceny.append(x)
            ceny.append("^")
            ceny.append(kat)
            ceny.append("^")
            ceny.append(net)
            # print(ceny)

            with open(r"C:\Users\Filip Kordusiak\Downloads\img.csv", 'a') as fi:
                writer = csv.writer(fi)
                writer.writerow(ceny)
        except:
            pass

    def search_page(self):
        self.browser.get(url3)
        self.browser.implicitly_wait(1)


class Test_csv(Test):

    def loading_page(self, elem):
        time.sleep(1)
        self.browser.get(url4)
        self.browser.implicitly_wait(1)
        self.browser.get(url5)  # przechodzi do strony bez koniecznosci otwierania do nowego oknas
        m5 = self.browser.find_element("name", 'partNO')
        self.browser.find_element("name", 'partNO').clear()
        m5.send_keys(elem)
        self.browser.find_element("name", "Display").click()
        self.browser.find_element("name", "Download Results").click()

    def download_file_and_rename(self):
        for i in range(0, 9):
            file_exists = os.path.exists(r"C:\Users\Filip Kordusiak\Downloads\Part_Models.xls")
            if not file_exists:
                time.sleep(1)
            else:
                break
        time.sleep(1)
        old_name = r"C:\Users\Filip Kordusiak\Downloads\Part_Models.xls"
        new_name = r"C:\Users\Filip Kordusiak\Downloads\123456789.csv"
        # Renaming the file
        try:
            os.rename(old_name, new_name)
        except:
            pass

    def csv_files(self, lista=None):
        with open(r"C:\Users\Filip Kordusiak\Downloads\123456789.csv", 'r') as file:
            reader = csv.reader(file, delimiter='\t')

            items_in_1 = list()
            next(reader)
            for row in reader:
                items_in_1.append(row[2])
            items_in_1.insert(0, '123;')
            # print(items_in_1)

            with open(r"C:\Users\Filip Kordusiak\Downloads\hhh.csv", 'a') as f:
                writer = csv.writer(f)

                writer.writerow(items_in_1)

        os.remove(r"C:\Users\Filip Kordusiak\Downloads\123456789.csv")
        # df = pd.DataFrame(items_in_1)
        # df.to_csv(r"C:\Users\Filip Kordusiak\Downloads\hhh.csv", sep='\t')


test = Test()

test.login_proces()
test.microsoft_conf()
# test.product(x)
# test.zdjecia(x)
# test.search_page()


test1 = Test_csv()

test1.login_proces()
x5 = ['3111040R92', '14142390', '10863090', '14148090', '14152090', '16739295', '114799A1GV', '120489687GV',
      '245531C91GV', '3116099R91GV']

for item in x5:
    start = time.time()
    test1.loading_page(item)
    test1.download_file_and_rename()
    try:
        test1.csv_files()
    except:
        pass
    end = time.time()
    print("test1", end - start)
    start1 = time.time()
    test.product(item)
    test.zdjecia(item)
    test.search_page()
    end1 = time.time()
    print("test2", end1 - start1)


