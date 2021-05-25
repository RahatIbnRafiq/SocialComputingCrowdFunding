from selenium import webdriver
import CONSTANTS
import time
import random


def fund_discoveries():
    options = webdriver.ChromeOptions()
    options.headless = True
    for category in CONSTANTS.CATEGORIES[1:10]:
        print("_____________________________________________")
        print("Collecting data for category: " + category)
        link_file = open(category+".txt", "w")
        driver = webdriver.Chrome(CONSTANTS.CHROME_DRIVER_PATH, options=options)
        driver.get(CONSTANTS.URL_ADDRESS + category)
        elems = driver.find_elements_by_css_selector(".react-campaign-tile [href]")
        links = set([elem.get_attribute('href') for elem in elems])
        prev_total_links = len(links)
        counter = 0
        try:
            while True:
                show_more_button = driver.find_element_by_link_text("Show More")
                show_more_button.click()
                sleep_randomly()
                elems = driver.find_elements_by_css_selector(".react-campaign-tile [href]")
                links = set([elem.get_attribute('href') for elem in elems])
                current_total_links = len(links)
                print("current_total_links: " + str(len(links)) + " and counter is " + str(counter))
                if prev_total_links == current_total_links:
                    print("All the links have been collected for category: " + category)
                    break
                prev_total_links = current_total_links
                counter += 1
        except Exception as e:
            print("Something bad happened! " + str(e))
        finally:
            driver.quit()

        sleep_randomly()
        driver.quit()
        for link in links:
            link_file.write(link+"\n")
        link_file.close()
        print("_____________________________________________")


def sleep_randomly():
    random_sleep = random.randint(20, 60)
    time.sleep(random_sleep)

fund_discoveries()

