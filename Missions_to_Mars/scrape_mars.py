import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', ** executable_path, headless=False)

def scrape():
    browser = init_browser()

    ### NASA Mars News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html

    soup = bs(html, 'html.parser')

    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_='content_title').get_text()
    news_p = article.find('div', class_='article_teaser_body').get_text()

    ### JPL Mars Space Images - Featured Image
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    browser.click_link_by_id('full_image')
    time.sleep(5)

    browser.click_link_by_partial_text('more info')

    html = browser.html
    img_soup = bs(html, 'html.parser')

    ft_img_url = img_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{ft_img_url}'

    ### Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html

    soup = bs(html, 'html.parser')

    tweet = soup.find('div', attrs= {
        'class': 'tweet',
        'data-name': 'Mars Weather'
    })
    mars_weather = tweet.find('p', class_='tweet-text').get_text()

    ### Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    html = browser.html

    table = pd.read_html(facts_url)
    mars_facts = table[0]

    mars_facts.columns = ['Description', 'Value']

    mars_facts.set_index('Description', inplace=True)

    mars_facts = mars_facts.to_html(classes='table table-striped')

    ### Mars Hemispheres
    hemisph_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisph_url)
    html = browser.html

    soup = bs(html, 'html.parser')

    hemisphere_img_urls = []

    links = soup.find('div', class_='result-list')
    hemispheres = links.find_all('div', class_='item')

    for hemi in hemispheres:
        title = hemi.find('h3').text
        title = title.replace('Enhanced', '')
        hemi_name = hemi.find('a')['href']
        hemi_url = f'https://astrogeology.usgs.gov/{hemi_name}'
        browser.visit(hemi_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        dls = soup.find('div', class_='downloads')
        image_url = dls.find('a')['href']
        hemisphere_img_urls.append({'title': title, 'image_url': image_url})

    
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_facts,
        'hemisphere_img_urls': hemisphere_img_urls
    }

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()