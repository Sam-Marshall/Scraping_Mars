
# coding: utf-8

# In[1]:
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser


# In[2]:
def scrape():

    newsUrl = 'https://mars.nasa.gov/news/'
    picUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    weatherUrl = 'https://twitter.com/marswxreport?lang=en'
    factsUrl = 'https://space-facts.com/mars/'
    hemisUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[3]:


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[4]:


    news_response = requests.get(newsUrl)


    # In[5]:


    news_soup = bs(news_response.text, 'html.parser')


    # In[6]:


    #print(news_soup.prettify())


    # In[7]:


    news_results = news_soup.body.find_all('div', class_='slide')
    #print(len(news_results))
    news_list = []


    # In[8]:


    counter = 1

    for result in news_results:
        title = result.find('div', class_='content_title').find('a').text.strip()
        body = result.find('div', class_='rollover_description_inner').text.strip()
        article_information = {
            'article number': counter,
            'article title' : title,
            'articly summary' : body
        }
        
        news_list.append(article_information)
        counter += 1
        
    #print(news_list)


    # In[9]:


    browser.visit(picUrl)


    # In[10]:


    pic_html = browser.html
    pic_soup = bs(pic_html, 'html.parser')

    pic_style = pic_soup.find('article', class_='carousel_item')['style']


    # In[11]:


    pic_style = pic_style.split("url")[1]
    pic_link = pic_style.split("'")[1]


    # In[12]:


    pic_link_final = 'https://www.jpl.nasa.gov' + pic_link
    #print(pic_link_final)


    # In[13]:


    weather_response = requests.get(weatherUrl)
    weather_soup = bs(weather_response.text, 'html.parser')
    #print(weather_soup.prettify())


    # In[40]:


    weather_results = weather_soup.find_all('div', class_='content')


    # In[41]:


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


    # In[43]:


    facts = pd.read_html(factsUrl)


    # In[52]:


    facts_df = facts[0]
    facts_df = facts_df.rename(columns={0 : 'Variable', 1 : 'Value'})
    facts_df = facts_df.set_index('Variable')
    facts_df


    # In[60]:


    facts_df.to_html('facts.html')
    html_facts_df = facts_df.to_html()
    html_facts_df = html_facts_df.replace('\n', '')
    html_facts_df


    # In[61]:


    browser.visit(hemisUrl)


    # In[64]:


    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')

    hemi_results = hemi_soup.find_all('div', class_='item')


    # In[73]:


    link_array = []
    title_array = []
    for result in hemi_results:
        title = result.find('h3').text
        link = 'https://astrogeology.usgs.gov' + result.find('a').attrs['href']
        link_array.append(link)
        title_array.append(title)


    # In[76]:


    final_hemi_img = []
    for link in link_array:
        browser.visit(link)
        link_html = browser.html
        soup = bs(link_html, 'html.parser')
        result = soup.find('div', class_='downloads').find('a').attrs['href']
        final_hemi_img.append(result)


    # In[78]:


    hemi_data = []
    for title, link in zip (title_array, final_hemi_img):
        info = {
            'Image Hemisphere Title' : title,
            'Image Hemisphere Link' : link
        }
        hemi_data.append(info)
    #print(hemi_data)


    # In[ ]:

    information = {
        'News' : news_list,
        'Weather' : weather_text,
        'Main Image' : pic_link_final,
        'Table HTML' : html_facts_df,
        'Hemisphere Data' : hemi_data
    }

    return information