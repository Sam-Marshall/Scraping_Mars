# Scraping_Mars

This application was built to scrape the latest information about Mars and display it in one location. The project is driven by a Python backend featuring a scraper built on Selenium Webdriver, BeautifulSoup, and Pandas with routing provided by Flask. The scraped data is stored in MongoDB via the Pymongo driver.

The live app can be found here: https://mars-update-center.herokuapp.com/

## Required Packages

- beautifulsoup4==4.6.0
- Flask==1.0.2
- Flask-PyMongo==2.1.0
- gunicorn==19.9.0
- pandas==0.23.0
- requests==2.18.4
- selenium==3.14.1
- lxml==4.2.1

- splinter==0.9.0 (*not used in the deployed app, but used during local development)

