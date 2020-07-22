"""Wordpress.com blog scraper v1.0
Should work on majority of wp blogs,
will scrape text and images and save
to a folder with blogs name.

By Steve Shambles 2018
updated nov 2019.

stevepython.wordpress.com

pip3 install beautifulsoup4
pip3 install requests
"""
import os
import re
from urllib.request import urlopen
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
import requests

BLOG2_SCRAPE = ''
POSTLINK = ''

def scrape_link():
    """Get the text body and images of links."""
    ht_ml = urlopen(POSTLINK)
    b_s = BeautifulSoup(ht_ml.read(), 'lxml')

    # find image urls and save links to text file
    with open('image_links.txt', 'a', encoding='utf-8') as file:

        png_images = b_s.find_all('img', {'src':re.compile('.png')})
        for image in png_images:
            image_link = (image['src'])
            print(image_link)
            file.write((image['src']))
            file.write('\n\n')

            #construct file_name from the posts url
            parsed = urlsplit(image_link)
            img_file_name = (parsed.path)
            #remove slashes, replace with dashes
            img_file_name = img_file_name.replace('/', '-')
            #remove a newline that always appears in this scrape
            img_file_name = img_file_name.replace('\n', '')
        try:
            #save png image to cwd
            with open(img_file_name, 'wb') as handle:
                response = requests.get(image_link, stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
        except:
            pass

        # Do jpg images
        jpg_images = b_s.find_all('img', {'src':re.compile('.jpg')})
        for image in jpg_images:
            image_link = (image['src'])
            file.write((image['src']))
            file.write('\n\n')

            #construct file_name from the posts url
            parsed = urlsplit(image_link)
            img_file_name = (parsed.path)
            #remove slashes, replace with dashes
            img_file_name = img_file_name.replace('/', '-')
            #remove a newline that always appears in this scrape
            img_file_name = img_file_name.replace('\n', '')

            #save jpg image to cwd
            with open(img_file_name, 'wb') as handle:
                response = requests.get(image_link, stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

    # -------------now for the text part of the post--------

    # Find the text content of the post.
    so_up = b_s.find_all('div', {'class':'entry-content'})
    # Some use entry-body instead.
    if not so_up:
        so_up = b_s.find_all('div', {'class':'entrybody'})
    # Some use post-entry.
    if not so_up:
        so_up = b_s.find_all('div', {'class':'post-entry'})
    # Some use post-entry.
    if not so_up:
        so_up = b_s.find_all('div', {'class':'entry'})
        # Some use main.
    if not so_up:
        so_up = b_s.find_all('div', {'class':'main'})

    # Construct file_name from the posts url.
    parsed = urlsplit(POSTLINK)
    file_name = (parsed.path)
    # Remove slashes, replace with dashes.
    file_name = file_name.replace('/', '-')
    # Remove a newline that always appears in this scrape.
    file_name = file_name.replace('\n', '')
    file_name = file_name +str('.txt')

    # save the post as a txt file
    for name in so_up:
        article = (name.get_text())
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(POSTLINK)
            file.write('\n\n')
            file.write(article)
            file.write('\n\n')

def create_folder():
    """Create a folder using blog name."""
    my_dir = (str(BLOG2_SCRAPE))
    my_dir = my_dir[: my_dir.find('.wordpress')]
    my_dir = my_dir.replace('https://', '')

    # If it doesn't exist then create it.
    check_folder = os.path.isdir(my_dir)
    if not check_folder:
        os.makedirs(my_dir)
        print('created folder : ' +my_dir)

    # Change dir to new folder.
    os.chdir(my_dir)

def scrape_sitemap():
    """Get all links from url (BLOG2_SCRAPE) via the sites sitemap.xml."""
    pa_ges = []

    req_uest = str(BLOG2_SCRAPE)+'sitemap.xml'
    f_w = urlopen(req_uest, timeout=3)
    xm_l = f_w.read()

    so_up = BeautifulSoup(xm_l, 'lxml')
    url_tags = so_up.find_all('url')

    # Output to shell, delete these 3 print lines if not required.
    print('Sitemap for:', req_uest)
    print('urls found:', str(len(url_tags)))
    print()

    # Save urls to a text file named links.txt to curr dir.
    with open('links.txt', 'w') as file:
        for sitemap in url_tags:
            link = sitemap.findNext('loc').text
            pa_ges.append(link)
            file.write(link)
            file.write('\n')
    f_w.close()

#tested and works on these blogs: un cooment one to try it.
#BLOG2_SCRAPE = 'https://19thcenturywellington.wordpress.com/'
#BLOG2_SCRAPE = 'https://stevepython.wordpress.com/'
#BLOG2_SCRAPE = 'https://hortonwhc.wordpress.com/'
#BLOG2_SCRAPE = 'https://humiliationstories.wordpress.com/'
#BLOG2_SCRAPE = 'https://palisadegranfondo.wordpress.com/'
#BLOG2_SCRAPE = 'https://southernmuslimah.wordpress.com/'
#BLOG2_SCRAPE = 'https://bfall2014.wordpress.com/'
#BLOG2_SCRAPE = 'https://usergeneratededucation.wordpress.com/'
#BLOG2_SCRAPE = 'https://ppverbeek.wordpress.com/'
#BLOG2_SCRAPE = 'https://sladersyard.wordpress.com/'
#BLOG2_SCRAPE = 'https://scaccodes.wordpress.com/'
BLOG2_SCRAPE = 'https://wordpress.com/block-editor/post/tinkerbotblog.wordpress.com/31/'
# Main.
create_folder()
scrape_sitemap()

#open text file of scraped links
#and call scrape_link for each link

with open('links.txt', encoding='utf-8') as f:
    for line in f:
        POSTLINK = line
        print(POSTLINK)
        scrape_link()

print()
print()
print("Finished Scrape.")
