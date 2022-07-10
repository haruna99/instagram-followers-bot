import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchFrameException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

INSTAGRAM_USERNAME = os.environ.get("INSTA_USER")
INSTAGRAM_PASSWORD = os.environ.get("INSTA_PASSWORD")
similar_account = "chefsteps"
insta_url = "https://www.instagram.com"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def login(self):
        self.driver.get(f"{insta_url}/accounts/login/")

        time.sleep(5)

        username = self.driver.find_element("name", "username")
        username.send_keys(INSTAGRAM_USERNAME)
        password = self.driver.find_element("name", "password")
        password.send_keys(INSTAGRAM_PASSWORD)
        password.send_keys(Keys.ENTER)

        time.sleep(3)

        self.driver.find_element("xpath", '//*[@id="react-root"]/section/'
                                          'main/div/div/div/div/button'
                                 ).click()

        time.sleep(5)

        self.driver.find_element("xpath", '/html/body/div[1]/div/div[1]/div'
                                          '/div[2]/div/div/div[1]/div/div[2]/div/div'
                                          '/div/div/div/div/div/div[3]/button[2]'
                                 ).click()

    def find_followers(self):
        time.sleep(2)

        self.driver.get(f"{insta_url}/{similar_account}")

        time.sleep(4)

        followers = self.driver.find_element("xpath", '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/'
                                                      'div[1]/div[1]/section/main/div/header/section/ul/li[2]/a'
                                             )
        followers.click()

        time.sleep(3)

        modal = self.driver.find_element("xpath", '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]'
                                                  '/div/div[2]/div/div/div/div/div/div/div/div[2]'
                                         )
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        follow_btn = self.driver.find_elements("css selector", "._aae- button")
        for btn in follow_btn:
            try:
                time.sleep(2)
                btn.click()
            except ElementClickInterceptedException:
                self.driver.find_element("xpath", '/html/body/div[1]/div/div[1]/div/div[2]/div/div'
                                                  '/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/'
                                                  'div/div/div/div[3]/button[2]'
                                         ).click()
                time.sleep(1)
                btn.click()


insta_follower = InstaFollower()
insta_follower.login()
insta_follower.find_followers()
insta_follower.follow()
