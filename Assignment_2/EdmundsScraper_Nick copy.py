import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
from itertools import izip_longest

ForumURL = "https://forums.edmunds.com/discussion/7526/general/x/midsize-sedans-2-0/p"

def Scraper(ForumURL, npages): # Input the number of pages you want to scrape.
    tableResults = []
    for page in (range(1, npages)):
        URL = ForumURL + str(page)
        print URL
        site_request = urllib2.Request(URL, headers={'User-Agent': "Magic Browser"})
        site_open = urllib2.urlopen(site_request)
        soup = BeautifulSoup(site_open, "lxml")

        userposts = soup.findAll("a", {'class': 'Username'})
        usernamesText = [userpost.string for userpost in userposts]

        dates = soup.findAll("time")
        datesText = [date['title'] for date in dates]

        posts = soup.findAll("div", {'class': 'Message'})
        posts_text = [post.text.encode('utf-8').strip() for post in posts]

        page_results = zip(usernamesText, datesText, posts_text) # Each post becomes a tuple.
        for result in page_results:
            tableResults.append(result) # Each tuple gets added to final list.
        page_results = []
    return tableResults


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


def toCSV(data):
    newData = []
    colnames = ["userid", "date", "message"]
    for y_tuple in data:
        for group_of_3 in grouper(y_tuple, 3):
            newData.append(list(group_of_3))
    return pd.DataFrame(data=newData, columns=colnames).to_csv("Edmunds Page Scrape.csv", sep=',')


toCSV(Scraper(ForumURL, npages=35))