import pymongo
import CarsScraperSingle as cars

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.usedCarsDB

search_collection = db.search_results

# print(cars.scrape())

search_collection.insert_many(cars.scrape())