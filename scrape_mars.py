# coding: utf-8
# author : Stacy Marshall October 2018

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape():

    #All the URLs I will be scraping from
    newsUrl = 'https://mars.nasa.gov/news/'
    picUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    weatherUrl = 'https://twitter.com/marswxreport?lang=en'
    factsUrl = 'https://space-facts.com/mars/'
    hemisUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Setting up either a Selenium or Splinter Chrome Webdriver
    
    #Comment out this block if you are running locally
    chrome_options = Options()
    chrome_options.binary_location = '/app/.apt/usr/bin/google-chrome'
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', chrome_options=chrome_options)
    ### End Comment out

    #Comment out this block if you are running on Heroku
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False)
    ### End Comment out

    #Getting Latest news from https://mars.nasa.gov/news/

    news_response = requests.get(newsUrl)
    news_soup = bs(news_response.text, 'html.parser')
    #print(news_soup.prettify())

    news_results = news_soup.body.find_all('div', class_='slide')
    #print(len(news_results))
    news_list = []
    counter = 1

    for result in news_results:
        title = result.find('div', class_='content_title').find('a').text.strip()
        body = result.find('div', class_='rollover_description_inner').text.strip()
        link = 'https://mars.nasa.gov' + result.find('a').attrs['href']

        article_information = {
            'article_number': counter,
            'article_title' : title,
            'article_summary' : body,
            'article_link' : link
        }
        
        news_list.append(article_information)
        counter += 1
    #print(news_list)

    #Getting featured image from https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

    #Comment out this block if you are running on Heroku
    #browser.visit(picUrl)
    #pic_html = browser.html
    ### End Comment Out

    #Comment out this block if you are running locally
    browser.get(picUrl)
    pic_html = browser.page_source
    ### End Comment Out

    pic_soup = bs(pic_html, 'html.parser')
    pic_style = pic_soup.find('article', class_='carousel_item')['style']
    pic_style = pic_style.split("url")[1]
    pic_link = pic_style.split("'")[1]
    pic_link_final = 'https://www.jpl.nasa.gov' + pic_link
    #print(pic_link_final)

    #Getting latest weather update from https://twitter.com/marswxreport?lang=en

    weather_response = requests.get(weatherUrl)
    weather_soup = bs(weather_response.text, 'html.parser')
    #print(weather_soup.prettify())
    weather_results = weather_soup.find_all('div', class_='content')

    weather_text = ''
    for result in weather_results:
        try:
            href = result.find('a').attrs['href']
            if href=='/MarsWxReport':
                content = result.find('div', class_='js-tweet-text-container').find('p').text.strip()
                if 'Sol' in content:
                    weather_text = content
                    break
        except AttributeError as error:
            print(error)
    #print(weather_text)

    #Getting general facts from https://space-facts.com/mars/

    facts = pd.read_html(factsUrl)
    facts_df = facts[0]
    facts_df = facts_df.rename(columns={0 : 'Variable', 1 : 'Value'})
    facts_df = facts_df.set_index('Variable')
    facts_df

    table_headers = list(facts_df.index.values)
    table_values = list(facts_df['Value'].values)

    table_data = []
    for header, value in zip (table_headers, table_values):
        info = {
            'Table_Headers' : header,
            'Table_Values' : value
        }
        table_data.append(info)

    facts_df.to_html('facts.html')
    html_facts_df = facts_df.to_html()
    html_facts_df = html_facts_df.replace('\n', '')
    #html_facts_df

    #Getting hemisphere images from https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

    #Comment out this block if you are running on Heroku
    #browser.visit(hemisUrl)
    #hemi_html = browser.html
    ### End Comment Out
    
    #Comment out this block if you are running locally
    browser.get(hemisUrl)
    hemi_html = browser.page_source
    ### End Comment Out

    hemi_soup = bs(hemi_html, 'html.parser')
    hemi_results = hemi_soup.find_all('div', class_='item')
    link_array = []
    title_array = []
    for result in hemi_results:
        title = result.find('h3').text
        link = 'https://astrogeology.usgs.gov' + result.find('a').attrs['href']
        link_array.append(link)
        title_array.append(title)

    final_hemi_img = []
    for link in link_array:
        
        #Comment out this block if you are running on Heroku
        #browser.visit(link)
        #link_html = browser.html
        ### End Comment Out

        #Comment out this block if you are running locally
        browser.get(link)
        link_html = browser.page_source
        ### End Comment Out

        soup = bs(link_html, 'html.parser')
        result = soup.find('div', class_='downloads').find('a').attrs['href']
        final_hemi_img.append(result)

    hemi_data = []
    for title, link in zip (title_array, final_hemi_img):
        info = {
            'Image_Hemisphere_Title' : title,
            'Image_Hemisphere_Link' : link
        }
        hemi_data.append(info)
    #print(hemi_data)

    #Organizing scraped data in a dictionary
    
    information = {
        'News' : news_list,
        'Weather' : weather_text,
        'Main_Image' : pic_link_final,
        'Table_Data' : table_data,
        'Hemisphere_Data' : hemi_data
    }

    return information