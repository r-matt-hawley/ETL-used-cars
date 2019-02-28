import pandas as pd 
from flask import Flask, jsonify, render_template, redirect
import pymongo
import CarsScraperSingle
import TrueCarScraper

app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.usedCarsDB

# mongo = pymongo(app, uri="mongodb://localhost:27017/usedCarsDB")


@app.route("/")
def index():

   landing_page = '''<h1>User Cars Search API</h1>
   <p> Available links<p>
   <p> /api/v1/allCar </p>
   <p> /api/v1/truecar</p>
   <p> /api/v1/cars </p>
   <p> /scrape </p>
   '''

   return landing_page

@app.route("/scrape")
def scrape():
   searchCars = CarsScraperSingle.scrape()
   searchTrueCar = TrueCarScraper.scrape()
   
   db.cars.insert_many(searchCars)
   db.trueCar.insert_many(searchTrueCar)

   #mongo.db.usedCarsDB({}, searchCars, upsert=True)

   return redirect("/")

@app.route("/api/v1/allCar")
def allCar():

   allCar = db.cars.find()+db.trueCar.find()
   #allCar.append(db.trueCar.find())

   return jsonify(list(allCar))

@app.route("/api/v1/truecar")
def trueCar():

   allCar = db.trueCar.find()

   return (allCar)

@app.route("/api/v1/cars")
def cars():

   allCar = db.cars.find()

   return jsonify(list(allCar['cars']))

if __name__ == "__main__":
   app.run(debug=True)