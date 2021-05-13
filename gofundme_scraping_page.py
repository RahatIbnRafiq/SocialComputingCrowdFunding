from selenium import webdriver
import CONSTANTS
import time
import random


def scrape_fundraiser_page():
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(CONSTANTS.CHROME_DRIVER_PATH, options=options)
    driver.get("https://www.gofundme.com/f/save-indian-trans-lives-covid-relief?"
               "utm_campaign=p_cp_url&utm_medium=os&utm_source=customer")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(5)
    page_source_element = driver.find_element_by_xpath("//div[@id='root']")
    #print(page_source_element.get_attribute('innerHTML'))
    campaign_comments = page_source_element.find_element_by_class_name('p-campaign-comments')
    print(campaign_comments.text)





    # raised = driver.find_element_by_class_name('m-progress-meter-heading')
    # created = driver.find_element_by_class_name('m-campaign-byline-created.a-created-date')
    # campaign_content = driver.find_element_by_class_name('p-campaign-content')
    # campaign_members = driver.find_element_by_class_name('p-campaign-members')
    # campaign_description = driver.find_element_by_class_name('p-campaign-description')
    # campaign_updates = driver.find_element_by_class_name('p-campaign-updates')








scrape_fundraiser_page()

