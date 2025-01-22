from selenium import webdriver
from selenium.webdriver.common.by import By  # for finding dimensions of screenshot
from reddit_grab import post1  # importing reddit post object
import time  # so webpage can load before screenshotting


def take_screenshot():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(post1.url)

    # for verification
    print("Url: " + post1.url)
    print("Post ID: " + post1.id)

    time.sleep(5)

    # dynamically inserts post id into xpath
    element = driver.find_element(by=By.XPATH, value=f"//*[@id='t3_{post1.id}']")
    element.screenshot("media/post_screenshot.png")
