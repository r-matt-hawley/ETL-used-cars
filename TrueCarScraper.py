import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs

# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path, headless=False)

# https://www.cars.com/vehicledetail/detail/762102222/overview/

def scrape():

    url = "https://www.truecar.com/used-cars-for-sale/listings/year-2017-max/location-houston-tx/?searchRadius=100&sort[]=price_desc"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    database = []

    boxInfoList = soup.find_all('div', attrs={"data-qa": "VehicleDetailsSm"})#.find_all("div",attrs={"data-qa":True})


    for res_counter in range(0, len(boxInfoList)):
        scraped = {}
        boxInfo = boxInfoList[res_counter].find_all("div",attrs={"data-qa":True})

    # Get all result info available
        for rez in boxInfo: 
            scraped[rez["data-qa"].split("-")[2]]=rez.text
            
        
        vin = soup.find_all("a", attrs={"data-qa": "VehicleListing"})[res_counter]["href"].split("/")[3]
        scraped["VIN"] = vin

        
        # Year, Make, Model, Price, and vehicle url are all in the same a tag.
        AutoListing = soup.find_all('a', attrs={"data-qa": "VehicleListing"})[res_counter]
        header = AutoListing.find_all("h4")[0].text.split(" ")
        scraped["Year"] = header[0]
        scraped["Make"] = header[1]
        scraped["Model"] = header[2]
        try:
            scraped["Model"] += f" {header[3]}"
        except IndexError:
            pass
        scraped["Price"] = AutoListing.find_all("h4")[1].text
        scraped["URL"] = "http://www.truecar.com" + AutoListing["href"]
        
        database.append(scraped)
        # End for loop
    return database

print(scrape())