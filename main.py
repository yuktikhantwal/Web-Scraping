# importations
import bs4
import html5lib
import csv
import time
from selenium import webdriver

# setting up driver to get the URL
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(executable_path=r"C:\webdrivers\chromedriver.exe",options=options)

# create csv file
file = open('books.csv','wt')
wr = csv.writer(file)

# write columns names 
wr.writerow(['Book Name',
             'Author Name',
             'Publisher Name',
             'List Price',
             'Selling Price',
             'Binding',
             'Release Date',
             'Language'])

# base link of all webpages
base_link = 'https://www.bookswagon.com/view-books'

# further link to each page
all_links = ['/0/new-arrivals',
             '/1/bestsellers',
             '/2/recently-sold',
             '/3/coming-soon-preorder-now',
             '/4/textbooks',
             '/5/award-winners',
             '/6/newyork-times-bestseller',
             '/7/staff-picks',
             '/8/box-sets']

# iterate for each page
for link in all_links:
    url = base_link + link

    driver.get(url)

    # for scrolling till page end
    page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
    stop = False
    while(stop==False):
        last_count = page_len
        time.sleep(3)
        page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
        if last_count==page_len:
            stop = True

    soup = bs4.BeautifulSoup(driver.page_source,'html5lib')

    # find all book elements on the page
    items = soup.find_all(class_='list-view-books')

    # iterate for each book element
    for item in items:
        # book name
        book_name_element = (item.find(class_="title")).find('a')
        book_name = 'Not mentioned' if book_name_element==None else book_name_element.text
        
        # author and publisher
        auth_publ_element = item.find_all(class_="author-publisher")
        auth_name = 'Not mentioned'
        publ_name = 'Not mentioned'
        if len(auth_publ_element)==2:
            auth_name = auth_publ_element[0].find('a').text
            publ_name = auth_publ_element[1].find('a').text
        elif len(auth_publ_element)==1:
            publ_name = auth_publ_element[0].find('a').text

        # list price
        list_price_element = item.find(class_="list")
        list_price = 'Not mentioned' if list_price_element==None else list_price_element.text

        # selling price
        sell_price_element = item.find(class_="sell")
        sell_price = 'Not mentioned' if sell_price_element==None else sell_price_element.text

        # binding, release date, language
        dictn = {
            'Binding:' : 'Not mentioned',
            'Release:' : 'Not mentioned',
            'Language:' : 'Not mentioned'
        }

        keys = item.find_all(class_="attributes-head")
        vals = item.find_all(class_="attributes-title")

        for key,val in zip(keys,vals):
            k = key.text
            v = val.text
            dictn[k] = v

        binding = dictn['Binding:']
        release_date = dictn['Release:']
        language = dictn['Language:']

        # add the book details to the csv file
        wr.writerow([book_name,
                     auth_name,
                     publ_name,
                     list_price,
                     sell_price,
                     binding,
                     release_date,
                     language])

# finally close the file
file.close()       