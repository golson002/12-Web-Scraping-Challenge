# Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Create empty mars_data dictionary to append our results to
mars_data = {}

def scrape_all():

    # Executable path + initialize browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# Scraping: NASA Mars News

    # NASA Mars News URL to scrape
    news_url = 'https://redplanetscience.com/'

    # Visit URL
    browser.visit(news_url)

    # Create HTML and Beautiful Soup Object
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')
    try:
        # Collect the latest news title
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_ = 'content_title').get_text()
    
        # Collect the latest paragraph text for the news title
        news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()

        # Append results to mars_data dictionary
        mars_data['news_title'] = news_title
        mars_data['news_p'] = news_p
    
    except AttributeError:
        # Append results to mars_data dictionary
        mars_data['news_title'] = None
        mars_data['news_p'] = None
        
# Scraping: JPL Mars Space Images- Featured Image

    # JPL Mars Space Images URL to scrape
    image_url = 'https://spaceimages-mars.com/'

    # Visit URL
    browser.visit(image_url)

    # Create HTML and Beautiful Soup Object
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    # Find all images with the 'img' selector
    all_images = image_soup.find_all('img')

    # Display the image source for each image found in all_images
    images = []
    for image in all_images:
        images.append(image['src'])

    # Merge the base URL and the image source to display the image URL for the current Featured Mars Image
    base_url = 'https://spaceimages-mars.com/'
    featured_image_url = base_url + images[1]

    # Append results to mars_data dictionary
    mars_data['featured_image_url'] = featured_image_url    


# Scraping: Mars Facts

    # Mars Facts URL to scrape
    facts_url = 'https://galaxyfacts-mars.com/'

    # Visit URL
    browser.visit(facts_url)

    # Use Pandas read_html to parse the url
    tables = pd.read_html(facts_url)
    tables

    # Create dataframe for facts table
    facts_df = tables[0]
    facts_df

    # Change column names and set index
    facts_df.columns = ['Description', 'Mars', 'Earth']
    facts_df.set_index('Description', inplace = True)
    facts_df

    # Convert the data to a HTML table string
    facts_html_table = facts_df.to_html()
    facts_html_table

    # Strip unwanted newslines to clean up the table
    facts_html_table.replace('\n','')

    # Save the table
    facts_df.to_html('mars_facts.html')

    # Append results to mars_data dictionary
    mars_data['facts_html_table'] = facts_html_table


# Scraping: Mars Hemispheres

    # Mars Hemispheres URL to scrape
    hemisphere_url = 'https://marshemispheres.com/'

    # Visit URL
    browser.visit(hemisphere_url + 'index.html')

    # Create HTML and Beautiful Soup Object
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')

    # Find all 'div' selectors that contain mars hemisphere information
    results = hemisphere_soup.find_all('div', class_ = 'item')

    # Create empty hemispheres data lists to append to 
    hemisphere_data = []

    # Base URL
    base_url = 'https://marshemispheres.com/'

    # Loop through the hemisphere data in 'results' and append the title and URL to the hemisphere_data list
    for item in results:
        hemisphere_title = item.find('h3').text
        img_url = item.find('a', class_ = 'itemLink product-item')['href']
        
        # Go to the hemisphere page to find the full-resolution image
        browser.visit(base_url + img_url)
        
        # Create HTML and Beautiful Soup Object
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        
        # Full image URL
        final_img_url = base_url + img_soup.find('img', class_ = 'wide-image')['src']
        
        # Append the title and full image URL to the hemisphere_data list in a dictionary format
        hemisphere_data.append({'title': hemisphere_title, 'img_url': final_img_url })
    
    # Append results to mars_data dictionary
    mars_data['hemisphere_data'] = hemisphere_data

    # Close the browser
    browser.quit()

    return mars_data

print(mars_data)

