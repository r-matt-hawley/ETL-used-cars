import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs

############################################
# Helper Function: Advance to next result. #
############################################
def next_result(browser):
    next_button = browser.find_by_css("a[data-linkname='vdp-next']").first
    next_url = next_button["href"]
    if next_url.split("/")[5] == "undefined":
        return False

    next_button.click()
    return next_url

def scrape():
    # Splinter Set Up
    ''' Make sure to use content manager, so that the broswer closes when finished scraping.'''
    ''' Don't use headless=True.  The response time is slower because of listening messages,
    and you won't be able to see your print statements in the terminal.'''

    # Mac
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    with Browser('chrome', **executable_path, headless=False) as browser: # Content Manager

    # Windows 
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # with Browser('chrome', **executable_path, headless=False) as browser: # Content Manager

        ##############################
        # Use Splinter to find pages #
        ##############################

        # Search URL:https://www.cars.com/for-sale/searchresults.action/?rd=30&searchSource=QUICK_FORM&stkTypId=28881&zc=77034
        url = 'https://www.cars.com/for-sale/searchresults.action/?rd=30&searchSource=QUICK_FORM&stkTypId=28881&zc=77034'
        browser.visit(url)

        # Navigate to first result.
        # Find href to click
        first_result = browser.find_by_css("div[class='shop-srp-listings__listing-container'] a").first

        # Save url to use in scraper.
        current_url = first_result["href"]

        first_result.click()

        # create Database
        database = []
        page_count = 1

        ######################
        # Scrape result page #
        ######################

        while(current_url != False):
        # while(page_count <= 20):
                
            # Set up Beautiful Soup
            response = requests.get(current_url)
            soup = bs(response.text, 'html.parser')

            # Scrape
            scraped = {}

            basic_info = soup.find_all('li', class_="vdp-details-basics__item")
            for res in basic_info:
                try:
                    scraped[res.strong.text[:-1]] = res.span.text.lstrip()
                    
                except AttributeError as e:
                    print(e)

            try:
                scraped["price"] = soup.find("div", class_="vehicle-info__price").span.text
                
                header = soup.find_all("h1")[0].text
                head_list = header.split(" ")
                scraped["Year"] = head_list[1]
                scraped["Make"] = head_list[2]
                scraped["Model"] = head_list[3] + " " + head_list[4]
                
                scraped["Seller"] = soup.find("div", class_="page-section--seller-details").h2.text[8:]
                scraped["Seller Address"] = soup.find("div", class_="seller-details-location__text").a["href"]
                scraped["URL"] = current_url

            except AttributeError as e:
                print(e)
            except IndexError as e:
                print("Page missing info\n\n", e)

            database.append(scraped)

            current_url = next_result(browser)
            # print(current_url)
            page_count += 1
        # End while

    return database
