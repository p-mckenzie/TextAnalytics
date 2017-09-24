from bs4 import BeautifulSoup
import urllib2
import re
from datetime import datetime

def extract_username(soup_page):
    ret_username = []
    raw_usernames_lst = soup_page.select('.Username')
    for rowno,row in enumerate(raw_usernames_lst):
        raw_username = row.get('href')
        if(raw_username == None):
            continue
        ret_username.append(raw_username.rsplit('/', 1)[-1])
    return(ret_username)

def extract_date_time(soup_page):
    ret_time = []
    ret_date = []
    raw_timestamp = soup_page.select('.DateCreated')
    for rowno,row in enumerate(raw_timestamp):
        raw_time_text = row.find('time').get('datetime')
        raw_date_time = raw_time_text.split('T')
        raw_date = raw_date_time[0]
        raw_time = raw_date_time[1].split('+')[0]
        ret_date.append(raw_date)
        ret_time.append(raw_time)
    return(ret_time,ret_date)

def extract_message(soup_page):
    ret_message = []
    raw_message = soup_page.select('.Message')
    for rowno,row in enumerate(raw_message):
        ret_message.append(row.text.encode('utf-8').strip())
    return(ret_message)


final_usernames = []
final_date = []
final_time = []
final_message = []

num_records = 10000
num_pages = num_records/30
string = "p"
webpg_ending = []
for i in range(num_pages):
    if(i == 0):
        continue
    webpg_ending.append(string+`i`)

url = 'https://forums.edmunds.com/discussion/2864/general/x/entry-level-luxury-performance-sedans'

for num,page in enumerate(webpg_ending):
    print('Processing page ' + str(num))
    page_url = url + '/' + page
    page_url_open = urllib2.urlopen(page_url)
    page_url_data_soup = BeautifulSoup(page_url_open)
    final_usernames.append(extract_username(page_url_data_soup))
    date_time_data = extract_date_time(page_url_data_soup)
    final_date.append(date_time_data[1])
    final_time.append(date_time_data[0])
    final_message.append(extract_message(page_url_data_soup))

final_usernames = [item for sublist in final_usernames for item in sublist]
final_date = [item for sublist in final_date for item in sublist]
final_time = [item for sublist in final_time for item in sublist]
final_message = [item for sublist in final_message for item in sublist]

import pandas as pd
edmunds_df = pd.DataFrame({
    'username' : final_usernames,
    'date' : final_date,
    'time' : final_time,
    'message' : final_message
})

edmunds_df.to_csv('General_Sedan.csv')
