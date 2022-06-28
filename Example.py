from Scweet.scweet import scrape
import json
import csv
from Scweet.user import get_user_information, get_users_following, get_users_followers

Details = ["Username", "Tweets Count", "Following Count", "Followers Count",
           "Joined date",
           "Birthday", "Location", "Website", "Description", "Lists "
                                                             "subscribed to",
                               "Topics Followed"]

# # scrape top tweets with the words 'covid','covid19' and without replies. the process is slower as the interval is
# # smaller (choose an interval that can divide the period of time betwee, start and max date) scrape english top
# # tweets geolocated less than 200 km from Alicante (Spain) Lat=38.3452, Long=-0.481006.
# data = scrape(words=['bitcoin', 'ethereum'], since="2021-10-01", until="2021-10-05", from_account=None, interval=1,
#               headless=False, display_type="Top", save_images=False, lang="en",
#               resume=False, filter_replies=False, proximity=False, geocode="38.3452,-0.481006,200km")
#
# # scrape top tweets of with the hashtag #covid19, in proximity and without replies. the process is slower as the
# # interval is smaller (choose an interval that can divide the period of time betwee, start and max date)
# data = scrape(hashtag="bitcoin", since="2021-08-05", until="2021-08-08", from_account=None, interval=1,
#               headless=True, display_type="Top", save_images=False,
#               resume=False, filter_replies=True, proximity=True)

# Get the main information of a given list of users
# These users belongs to my following. 

users = ['nbrsr']

# this function return a list that contains : 
# ["nb of following","nb of followers", "join date", "birthdate", "location", "website", "description"]


#
# print(users_info)
# Get followers and following of a given list of users Enter your username and password in .env file. I recommande
# you dont use your main account. Increase wait argument to avoid banning your account and maximise the crawling
# process if the internet is slow. I used 1 and it's safe.

# set your .env file with SCWEET_EMAIL, SCWEET_USERNAME and SCWEET_PASSWORD variables and provide its path
# env_path = ".env"
#
file_names = get_users_following(users=users, env='.env', verbose=0,
                                headless=False, wait=3, file_path=None,
                                 follow_items=['followers'])

# file_names = ['outputs/shotrobin_user_1656154253793.7888_following.json',
#               'outputs/shotrobin_user_1656154253793.7888_followers.json']

# file_names = ['outputs/test_followers.json']
for each_file in file_names:
    fol_val = ''
    follower = False
    if 'following' in each_file:
        following = True
        fol_val = 'following_users_detail'
    elif 'follower' in each_file:
        follower = True
        fol_val = 'follower_users_detail'
    with open(each_file) as f:
        data = json.load(f)
        for key, value in data.items():
            users_info = get_user_information(key, fol_val, value,
                                              headless=False)
            file_name = 'outputs/{}_{}.csv'.format(key, fol_val)
            with open(file_name, 'w') as f:
                write = csv.writer(f)
                write.writerow(Details)
                write.writerows(users_info)
            #
# followers = get_users_followers(users=users, env='.env', verbose=0,
#                                 headless=False, wait=1, limit=50, file_path=None)
