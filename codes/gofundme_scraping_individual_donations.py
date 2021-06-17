from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = "/Users/rahatibnrafiq/chromedrivers_selenium/chromedriver"
URL_ADDRESS = "https://www.gofundme.com/discover/medical-fundraiser"


def scroll_down5():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get("https://www.gofundme.com/f/help-fight-against-censorship-complete-new-album")
    driver.find_element_by_partial_link_text("See all").click()

    try:
        pop_up_window = WebDriverWait(
            driver, 2).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='o-modal-donations-content']")))
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up_window)
            donations = pop_up_window.find_elements_by_class_name("o-donation-list-item")
            print(len(donations))
            for donation in donations:
                print(donation.text)
            time.sleep(1)
            break
    finally:
        driver.quit()

    time.sleep(3)
    driver.quit()


def donations_page_scraping():
    scroll_down5()


def fund_discoveries():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(URL_ADDRESS)
    elems = driver.find_elements_by_css_selector(".react-campaign-tile [href]")
    links = set([elem.get_attribute('href') for elem in elems])

    counter = 0

    try:
        while True:
            show_more_button = driver.find_element_by_link_text("Show More")
            show_more_button.click()
            time.sleep(10)
            elems = driver.find_elements_by_css_selector(".react-campaign-tile [href]")
            links = set([elem.get_attribute('href') for elem in elems])
            print("total links" + str(len(links)) +" and counter is " + str(counter))
            counter += 1
    finally:
        driver.quit()

    driver.quit()


donations_page_scraping()

