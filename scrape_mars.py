from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
from selenium import webdriver
from time import sleep


#def init_browser():
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape_info():

       # Run the function below:
    news_title, news_p = mars_news(browser)
    
       # Run the functions below and store into a dictionary
    results = {
            "title": news_title,
            "paragraph": news_p,
            "image_URL": jpl_image(browser),
            "weather": mars_weather(browser),
            "facts": mars_facts(),
            "hemispheres": mars_hemispheres(browser)
        }
   
        # Quit the browser and return the scraped results
    browser.quit()
    return results

def mars_news(browser):
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    news_title = news_soup.find('div', class_='content_title').find('a').text
    news_p = news_soup.find('div', class_='article_teaser_body').text

    
    return news_title, news_p

def jpl_image(browser):
       
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(5)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    featured_image_route = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_route}'

    return featured_image_url

def mars_weather(browser):

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    twitter_soup = BeautifulSoup(html, 'html.parser')

    mars_weather = twitter_soup.find('p', class_='TweetTextSize').text

    
    return mars_weather

def mars_facts():
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]
    df.columns =['description','value']
    df.set_index('description', inplace=True)
    html_table = df.to_html()
    
    
    return html_table

def mars_hemispheres( browser):
       
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # HTML Object
    html_hemispheres = browser.html
    # Parse HTML with Beautiful Soup
    hemp_soup = BeautifulSoup(html_hemispheres, 'html.parser')
    # Retreive all items that contain mars hemispheres information
    items = hemp_soup.find_all('div', class_='item')
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    # Store the main_url 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
        # Loop through the items previously stored
    for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    
    return hemisphere_image_urls







    

