import scraper
import dataParser
import os
import influencers
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user=input()
    print(scraper.scrape_user(user))

