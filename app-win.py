import pandas as pd 
from flask import Flask, jsonify, render_template, redirect
import pymongo
import CarsScraperSingleWin
import TrueCarScraper
import json

app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.usedCarsDB
cars_collection = db.cars
trueCar_collection = db.trueCar

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
   searchCars = CarsScraperSingleWin.scrape()
   searchTrueCar = TrueCarScraper.scrape()
   
   cars_collection.insert_many(searchCars)
   trueCar_collection.insert_many(searchTrueCar)

   return redirect("/")

@app.route("/api/v1/allCar")
def allCar():

   allCars = list(cars_collection.find())

   for car in trueCar_collection.find():
      allCars.append(car)

   # Remove id from each record before converting to JSON
   for car in allCars:
      car.pop("_id")

   return jsonify(allCars)

@app.route("/api/v1/truecar")
def trueCar():

   allCars = list(trueCar_collection.find())

   # Remove id from each record before converting to JSON
   for car in allCars:
      car.pop("_id")

   return jsonify(allCars)

@app.route("/api/v1/cars")
def cars():

   allCars = list(cars_collection.find())

   # Remove id from each record before converting to JSON
   for car in allCars:
      car.pop("_id")

   return jsonify(allCars)

if __name__ == "__main__":
   app.run(debug=True)