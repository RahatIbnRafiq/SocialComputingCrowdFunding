from selenium import webdriver
import CONSTANTS
import time
from Campaign import Campaign
from Comment import Comment
import random
import sys


def get_full_campaign_description(driver, campaign, logfile):
    campaign_description = None
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        sleep_randomly()
        driver.execute_script("window.scrollTo(0, 600);")
        sleep_randomly()
        while True:
            try:
                page_source_element = driver.find_element_by_xpath("//div[@id='root']")
                campaign_description = page_source_element.find_element_by_class_name('p-campaign-description')
                read_more_button = campaign_description.find_element_by_css_selector\
                    ('button.a-text-button.a-base-button')
                read_more_button.click()
                page_source_element = driver.find_element_by_xpath("//div[@id='root']")
                campaign_description = page_source_element.find_element_by_class_name('p-campaign-description')
                driver.execute_script("window.scrollTo(0, window.scrollY + 400)")
                sleep_randomly()
            except Exception as e:
                print("No read more any more. Got full campaign description." + str(e))
                break
            finally:
                if campaign_description is not None:
                    campaign.campaign_description = campaign_description.text
    except Exception as e:
        print("Something bad happened when getting campaign description: " + str(e))
        logfile.write("Something bad happened when getting campaign description: " + str(e) + "\n")


def get_campaign_update(driver, campaign, logfile):
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        sleep_randomly()
        driver.execute_script("window.scrollTo(0, 1500);")
        sleep_randomly()
        more_updates_button = \
            driver.find_element_by_css_selector('button.m-update-see-older-button.color-gray-60.text-small.a-text-button.a-base-button')
        driver.execute_script("arguments[0].scrollIntoView();", more_updates_button)
        more_updates_button.click()
        sleep_randomly()
        page_source_element = driver.find_element_by_xpath("//div[@id='portal']")
        update_list = page_source_element.find_element_by_class_name("o-updates-modal-list.list-unstyled")
        items = update_list.find_elements_by_tag_name("li")
        for item in items:
            item_text = str(item.text)
            item_text = item_text.strip().replace("\n", ", ")
            campaign.updates.append(item_text)
    except Exception as e:
        print("Exception while getting updates " + str(e))
        logfile.write("Exception while getting updates " + str(e) + "\n")


def collect_comments(driver, comments_dictionary):
    page_source_element = driver.find_element_by_xpath("//div[@id='root']")
    campaign_comments = page_source_element.find_element_by_class_name('p-campaign-comments')
    comments = campaign_comments.find_elements_by_class_name("o-comments-list-item")
    print(len(comments))
    for comment_id in range(0, len(comments)):
        if comment_id in comments_dictionary:
            continue
        comment_text = comments[comment_id].text
        comment_object = Comment(comment_text)
        comments_dictionary[comment_id] = comment_object


def get_campaign_comments(driver, campaign, logfile):
    comments_dictionary = {}
    prev_comment_count = 0
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep_randomly()
        while True:
            try:
                show_more_button = \
                    driver.find_element_by_css_selector\
                        ('button.mt2x.a-button.a-button--full-for-small.a-button--medium.a-button--hollow-green')
                show_more_button.click()
                collect_comments(driver, comments_dictionary)
                driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
                print("Comments Collected So Far : " + str(len(comments_dictionary)))
                if len(comments_dictionary) == prev_comment_count:
                    break
                prev_comment_count = len(comments_dictionary)
                time.sleep(10)
            except Exception as e:
                print("something bad happening when clicking for show more : " + str(e))
                collect_comments(driver, comments_dictionary)
                break
    except Exception as e:
        print("Something bad happened when getting campaign comments: " + str(e))
        logfile.write("Something bad happened when getting campaign comments: " + str(e) + "\n")
    finally:
        campaign.comments = comments_dictionary


def get_campaign_information(driver, campaign, logfile):
    try:
        page_source_element = driver.find_element_by_xpath("//div[@id='root']")
        raised = page_source_element.find_element_by_class_name('m-progress-meter-heading')
        created = page_source_element.find_element_by_class_name('m-campaign-byline-created.a-created-date')
        campaign_content = page_source_element.find_element_by_class_name('p-campaign')

        campaign.raised_text = raised.text.strip()
        campaign.created_text = created.text.strip()
        campaign.campaign_content_text = campaign_content.text.strip()
    except Exception as e:
        print("Exception when getting campaign information: " + str(e))
        logfile.write("Exception when getting campaign information: " + str(e) + "\n")


def get_top_donations(driver, campaign, logfile):
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        sleep_randomly()
        donors_button = driver.find_element_by_css_selector(
                'button.text-stat.disp-inline.text-left.a-button.a-button--inline')
        donors_button.click()
        sleep_randomly()
        page_source_element = driver.find_element_by_xpath("//div[@id='portal']")
        total_donations = page_source_element.find_element_by_class_name("o-modal-donations-header-title-row")

        # total_donations_text = total_donations.text
        # index1 = total_donations_text.index("(") + len("(")
        # index2 = total_donations_text.index(")")
        # total_donations_text = total_donations_text[index1:index2]
        # campaign.total_donations = total_donations_text

        campaign.total_donations_text = total_donations.text.strip()

        top_donations_button = driver.find_element_by_css_selector(
            'button.a-button.a-button--inline.a-button--small.a-button--white-shadow')
        top_donations_button.click()
        sleep_randomly()
        update_list = page_source_element.find_element_by_class_name\
            ("list-unstyled.o-donation-list")
        items = update_list.find_elements_by_tag_name("li")
        for item in items:
            item_text = str(item.text)
            item_text = item_text.strip().replace("\n", ", ")
            if len(item_text) < 10:
                continue
            campaign.top_donations.append(str(item_text))
        sleep_randomly()
        close_button = page_source_element.find_element_by_class_name("text-underline.a-button.a-button--inline")
        close_button.click()
    except Exception as e:
        print("Exception when getting top donations " + str(e))
        logfile.write("Exception when getting top donations " + str(e) + "\n")


def get_campaign_media(driver, campaign, logfile):
    try:
        page_source_element = driver.find_element_by_xpath("//div[@id='root']")
        try:
            video_element = page_source_element.find_element_by_class_name\
                ('m-video-iframe').get_attribute("src")
            campaign.campaign_video = video_element
        except Exception as e:
            print(" No video element found")

        try:
            image_element = page_source_element.find_element_by_class_name\
                ('a-image.a-image--background').get_attribute("style")
            campaign.campaign_image = image_element
        except Exception as e:
            print(" No image element found")
    except Exception as e:
        print("No media element found for this campaign: " + str(e))
        logfile.write("No media element found for this campaign: " + str(e) + "\n")


def sleep_randomly():
    random_sleep = random.randint(3, 7)
    time.sleep(random_sleep)


def scrape_fundraiser_page(link, driver, logfile):
    try:
        campaign = Campaign(link)
        driver.get(campaign.campaign_url)

        try:
            print("Getting Campaign Information...")
            get_campaign_information(driver, campaign, logfile)
            print("Campaign Information Done!")
        except Exception as e:
            print()

        try:
            print("Getting Campaign Media...")
            get_campaign_media(driver, campaign, logfile)
            print("Campaign Media Done!")
        except Exception as e:
            print()

        try:
            print("Getting Campaign Top Donations...")
            get_top_donations(driver, campaign, logfile)
            print("Campaign Top Donations Done!")
        except Exception as e:
            print()

        try:
            print("Getting Campaign Description...")
            get_full_campaign_description(driver, campaign, logfile)
            print("Campaign Description Done!")
        except Exception as e:
            print()

        try:
            print("Getting Campaign Comments...")
            get_campaign_comments(driver, campaign, logfile)
            print("Campaign Comments Done!")
        except Exception as e:
            print()

        try:
            print("Getting Campaign Updates...")
            get_campaign_update(driver, campaign, logfile)
            print("Campaign Update Done!")
        except Exception as e:
            print()
        campaign.print_log()
        campaign.write_to_file()

    except Exception as e:
        print("something bad happened for link : " + str(link) + "Exception is: " + str(e))
        logfile.write("something bad happened for link : " + str(link) + "Exception is: " + str(e) + "\n")


def get_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("disable-popup-blocking")
    options.add_argument("window-size=1680,940")
    driver = webdriver.Chrome(CONSTANTS.CHROME_DRIVER_PATH, options=options)
    driver.maximize_window()
    return driver


def scrape_fundraiser_pages(links):
    driver = get_driver()
    links_done = 0
    logfile = open("logfile.txt", "w")
    for link in links:
        try:
            print("___________________________________________________")
            logfile.write("___________________________________________________" + "\n")
            print("Collecting data for : " + str(link))
            logfile.write("Collecting data for : " + str(link) + "\n")
            scrape_fundraiser_page(link, driver, logfile)
            print("Collecting data for : " + str(link) + " is Done!")
            logfile.write("Collecting data for : " + str(link) + " is Done!" + "\n")
            links_done += 1
            print("Total links done: " + str(links_done))
            logfile.write("Total links done: " + str(links_done) + "\n")
            print("___________________________________________________")
        except Exception as e:
            driver.quit()
            driver = get_driver()
    logfile.close()


def get_links_to_scrape(start, end):
    all_links = []
    f = open("all_gofundme_links", "r")
    for line in f:
        all_links.append(line.strip())
    f.close()
    return all_links[start:end]
    # all_links = ["https://www.gofundme.com/f/2a7453y49c"]
    # return all_links


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. start and end index for the all_gofundme_links file")
    else:
        start, end = int(sys.argv[1]), int(sys.argv[2])
        links = get_links_to_scrape(start, end)
        scrape_fundraiser_pages(links)

