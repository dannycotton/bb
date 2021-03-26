import os
import threading
import time
import unittest
import json
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

class TestRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
      chrome_options = Options()
      chrome_options.add_argument("--headless")
        
      cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        
# Number 1
    def test_correct_address(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.amazon.com/sp?seller=A2N51X1QYGFUPK")
        address = wait.until(presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/ul/li[2]/span/ul/li[1]/span")))
        
        self.assertEqual('2800 Pringle Rd SE Suite 100', address.get_attribute("textContent"))

# Number 2
    def test_search_bar(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.bookbyte.com/advancedsearch.aspx")
        self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_tbKeywords").send_keys("college" + Keys.RETURN)
        searchResult = wait.until(presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_lbSearchedFor")))
        searchNumber = wait.until(presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_lblTotalResults")))

        self.assertEqual('college', searchResult.get_attribute("textContent"))
        self.assertLess(0, int(searchNumber.get_attribute("textContent")))

# Number 3
    def test_authors(self):
        bookInfo = json.load(urlopen("https://www.googleapis.com/books/v1/volumes?q=isbn:0131103628"))
        authors = bookInfo["items"][0]["volumeInfo"]["authors"]
        
        self.assertEqual('Brian W. Kernighan', authors[0])
        self.assertEqual('Dennis M. Ritchie', authors[1])

if __name__ == '__main__':
    unittest.main()
    #print ("all done tests ran" )