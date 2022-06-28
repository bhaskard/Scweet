from . import utils
from time import sleep
import random
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_user_information(key, fol_val, users, driver=None, headless=True):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)

    users_info = []

    skipped_users = []

    utils.log_in(driver, env='.env')
    for i, user in enumerate(users):

        log_user_page(user, driver)
        if user is not None:
            try:
                following = driver.find_element(by=By.XPATH,
                                     value='//a[contains(@href,'
                                           '"/following")]/span[1]/span[1]').text
                # following = driver.find_element_by_xpath(
                #     '//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath(
                    '//a[contains(@href,"/followers")]/span[1]/span[1]').text
            except Exception as e:
                # log_user_page(user, driver)
                # headers = driver.execute_script(
                #     "var req = new XMLHttpRequest();req.open('GET', "
                #     "document.location, false);req.send(null);return req.getResponseHeader('x-rate-limit-reset')")
                # rate_limit_sec = headers.splitlines()[0]
                # cur_time = time.time()
                # remaining = int((rate_limit_sec - cur_time ) / 1000)
                # sleep(remaining + 2)
                print("waiting")
                print(time.time())
                sleep(960)
                print(time.time())
                # driver.close()
                driver.quit()
                sleep(3)
                driver = utils.init_driver(headless=headless)
                utils.log_in(driver, env='.env')
                print("Failed {}".format(user))
                print(e)
                skipped_users.append(user)
                continue

            try:
                element = driver.find_element_by_xpath('//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                website = element.get_attribute("href")
            except Exception as e:
                # print(e)
                website = ""

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                # print(e)
                desc = ""
            a = 0
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                birthday = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                location = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
            except Exception as e:
                # print(e)
                try:
                    join_date = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    span1 = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                    if hasNumbers(span1):
                        birthday = span1
                        location = ""
                    else:
                        location = span1
                        birthday = ""
                except Exception as e:
                    # print(e)
                    try:
                        join_date = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        birthday = ""
                        location = ""
                    except Exception as e:
                        # print(e)
                        join_date = ""
                        birthday = ""
                        location = ""
            tweet_count = 0
            try:
                tweet_value = driver.find_element_by_xpath("//div[contains("
                                                          "text(), "
                                             "'Tweets')]").text
                tweet_count = str(tweet_value).split(" ")[0]
            except Exception as e:
                tweet_count = 0
                print("failed to get tweet count")
            print("--------------- " + user + " information : ---------------")
            join_date = join_date.replace("Joined ", "")
            print("Tweet count : ", tweet_count)
            print("Following : ", following)
            print("Followers : ", followers)
            print("Location : ", location)
            print("Join date : ", join_date)
            print("Birth date : ", birthday)
            print("Description : ", desc)
            print("Website : ", website)



            topic_names = []
            topic_descs = []
            try:
                log_user_topics_page(user, driver)
                _topic_names = driver.find_elements(by=By.XPATH,
                                                value="//*[contains(@id,'topic-name')]")

                # _topic_descs = driver.find_elements(by=By.XPATH,
                #                                     value="//*[contains(@id,"
                #                                           "'topic-description')]")
                for topic_name in _topic_names:
                    topic_names.append(topic_name.text)

                # for topic_desc in topic_descs:
                #     topic_descs.append(topic_desc.text)
                # print("topic_desc : ", topic_descs)
                print("topic_names : ", topic_names)
            except Exception as e:
                # print(e)
                print("Failed {}".format(user))
                print(e)
                skipped_users.append(user)
                topic_names = []
                topic_descs = []


            list_items = []
            try:
                log_user_list_page(user, driver)
                list_lists = driver.find_elements(by=By.XPATH,
                                                    value="//*[contains(@data-testid,'cellInnerDiv')]")

                for each_list in list_lists:
                    list_names = each_list.find_elements(by=By.XPATH,
                                         value=".//div[@dir='auto']/span[1]")
                    if len(list_names) > 1:
                        list_items.append(list_names[0].text)
                print("list_items : ", list_items)
            except Exception as e:
                print("Failed {}".format(user))
                print(e)
                skipped_users.append(user)
                print(e)
                list_items = []

            users_info.append([user, tweet_count, following, followers,
                               join_date, birthday,
                                location, website, desc, list_items,
                               topic_names])
            if i == len(users) - 1:
                file_name = 'outputs/{}_{}_missed_users.csv'.format(key,
                                                                   fol_val)
                with open(file_name, 'w') as f:
                    json.dump(skipped_users, f)
                    print(f"file saved in {file_name}")
                driver.close()
                return users_info
        else:
            print("You must specify the user")
            continue


def log_user_page(user, driver, headless=True):
    time.sleep(2)
    driver.get('https://twitter.com/' + user)
    time.sleep(4)
def log_user_list_page(user, driver, headless=True):
    time.sleep(2)
    driver.get('https://twitter.com/' + user + '/lists')
    time.sleep(4)


def log_user_topics_page(user, driver, headless=True):
    time.sleep(2)
    driver.get('https://twitter.com/' + user + '/topics')
    time.sleep(4)


def get_users_followers(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    followers = utils.get_users_follow(users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(followers, f)
        print(f"file saved in {file_path}")
    return followers


def get_users_following(users, env, verbose=1, headless=True, wait=2,
                        limit=float('inf'), file_path=None, follow_items=['following', 'followers']):
    # initiate the driver
    driver = utils.init_driver(headless=headless, env=env, firefox=True)
    sleep(wait)
    # log in (the .env file should contain the username and password)
    # driver.get('https://www.twitter.com/login')
    utils.log_in(driver, env, wait=wait)
    sleep(wait)
    tim = time.time() * 1000
    file_names = []
    for each_item in follow_items:
        file_name = 'shotrobin_user_{}_{}.json'
        following = utils.get_users_follow(driver, users, headless, env,
                                           each_item,
                                           verbose, wait=wait, limit=limit)
        file_path = 'outputs/' + file_name.format(tim, each_item)
        with open(file_path, 'w') as f:
            json.dump(following, f)
            print(f"file saved in {file_path}")
        file_names.append(file_path)
    return file_names


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
