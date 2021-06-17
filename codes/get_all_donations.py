from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys

CHROME_DRIVER_PATH = "/Users/rahatibnrafiq/chromedrivers_selenium/chromedriver"
#CHROME_DRIVER_PATH = "/usr/bin/chromedriver"


def sleep_randomly():
    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)


def element_exists(html, element):
    try:
        button = html.find_element_by_css_selector(element)
        return True
    except Exception:
        return False


def get_all_donations(fund_link):
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    driver.maximize_window()
    try:
        driver.get(fund_link)
        sleep_randomly()
        driver.find_element_by_partial_link_text("See all").click()
        pop_up_window = WebDriverWait(
            driver, 2).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='o-modal-donations-content']")))
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up_window)
            time.sleep(0.5)
            donations = pop_up_window.find_elements_by_class_name("o-donation-list-item")
            print("Donations till now: " + str(len(donations)))
            if element_exists(pop_up_window, "button.hrt-text-button.hrt-base-button"):
                print("Done collecting all donations!")
                break
        donations = pop_up_window.find_elements_by_class_name("o-donation-list-item")
        # print("Total Donations collected : " + str(len(donations)))
        all_donations = []
        for donation in donations:
            d = dict()
            try:
                person_name = donation.find_element_by_class_name("m-person-info-name")
                d["username"] = person_name.text
                items = donation.find_elements_by_class_name("m-meta-list-item")
                d["amount"] = items[0].text
                d["time"] = items[1].text
                all_donations.append(d)
            except Exception:
                continue
        return all_donations
    finally:
        driver.quit()


def collect_all_donations(start, end):
    f = open("all_gofundme_links.txt", "r")
    fund_links = []
    for line in f:
        fund_links.append(line.strip())
    f.close()
    for i in range(start, end):
        print("--------------------------------------------------------")
        fund_raiser = dict()
        fund_link = fund_links[i]
        print("collecting for " + str(i) + " th fund: " + fund_link)
        try:
            all_donations = get_all_donations(fund_link)
        except Exception:
            continue
        f = open("donations_" + str(i) + ".txt", "w")
        fund_raiser["url"] = fund_link
        fund_raiser["donations"] = all_donations
        f.write(str(fund_raiser) + "\n")
        f.close()
        print("total donations for this: " + str(len(all_donations)))
        print("Going to sleep for a bit")
        sleep_randomly()
        print("--------------------------------------------------------")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. start and end index for the all gofundme links file")
    else:
        start, end = int(sys.argv[1]), int(sys.argv[2])
        collect_all_donations(start, end)
