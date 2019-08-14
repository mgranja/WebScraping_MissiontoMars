from flask import Flask, render_template, redirect, url_for
#from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_news"
#mongo = PyMongo(app)

conn = "mongodb://localhost:27017/mars_db"
client = pymongo.MongoClient(conn)
client.db.mars.drop()


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    # @TODO: YOUR CODE HERE!
    #news_data = mongo.db.news_data.find_one()
    mars = client.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = client.db.mars
    mars_data = scrape_mars.scrape_info()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code =302)
    

    #news_data = mongo.db.news_data
    # Run the scrape function and save the results to a variable
    #news= scrape_mars.scrape_info()
    # Update the Mongo database using update and upsert=True
    #news_data.update({}, news, upsert=True)
    # Redirect back to home page


if __name__ == "__main__":
    app.run(debug=True)

                     