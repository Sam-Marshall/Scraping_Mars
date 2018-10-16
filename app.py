import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def home():
	mars_information = mongo.db.collection.find()
	return render_template("index.html", info=mars_information)

@app.route('/scrape')
def scrape():
	mars_scrape = scrape_mars.scrape()
	print(mars_scrape)
	mongo.db.collection.insert_one(mars_scrape)
	return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)