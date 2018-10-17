import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://heroku_f8tkdthf:m0eogdsjs3jcf6uf52sodpg9k7@ds135233.mlab.com:35233/heroku_f8tkdthf"
mongo = PyMongo(app)

@app.route('/')
def home():
	for doc in mongo.db.collection.find().sort("_id", pymongo.DESCENDING).limit(1):
		mars_information = doc
		news = mars_information['News']
		hemi = mars_information['Hemisphere_Data']
		table = mars_information['Table_Data']
	return render_template("index.html", info=mars_information, news=news, hemi=hemi,table=table)

@app.route('/scrape')
def scrape():
	mars_scrape = scrape_mars.scrape()
	mongo.db.collection.insert_one(mars_scrape)
	return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)