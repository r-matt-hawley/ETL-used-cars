import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs

!which chromedriver

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# https://www.cars.com/vehicledetail/detail/762102222/overview/
    
url = "https://www.truecar.com/used-cars-for-sale/listings/year-2017-max/location-houston-tx/?searchRadius=100&sort[]=price_desc"
response = requests.get(url)
soup = bs(response.text, 'html.parser')

scraped = {}

boxInfoList = soup.find_all('div', attrs={"data-qa": "VehicleDetailsSm"})#.find_all("div",attrs={"data-qa":True})

for box in boxInfoList:
    boxInfo = box.find_all("div",attrs={"data-qa":True})

# Get color ingo
    for rez in boxInfo: 
        scraped[rez["data-qa"].split("-")[2]]=rez.text
        

        vin = soup.find_all("a", attrs={"data-qa": "VehicleListing"})[0]["href"].split("/")[3]
    print(vin)
    scraped["VIN"] = vin

    results = soup.find('a', attrs={"data-qa": "VehicleListing"})

    AutoListing = results.find_all("h4")

    header = AutoListing[0].text.split(" ")
    scraped["Year"] = header[0]
    scraped["Make"] = header[1]
    scraped["Model"] = header[2]
    try:
        scraped["Model"] += f" {header[3]}"
    except IndexError:
        pass
    scraped["Price"] = AutoListing[1].text

