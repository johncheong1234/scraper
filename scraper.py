import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse,urljoin
from googlesearch import search

URL = "https://www.physiox.com.sg/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# convert to string
soup_string = str(soup)
# print(soup_string)

# create a function that takes in a string and returns a list of all email addresses in the string

def find_gmails(string):
    gmail_regex = r"\b[A-Za-z0-9._%+-]+@gmail\.com\b"
    gmail_emails = re.findall(gmail_regex, string)
    return list(set(gmail_emails))

def find_emails(string):
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    emails = re.findall(email_regex, string)
    # ensure only unique emails are returned
    return list(set(emails))

def get_subpages(url):
    subpages = set()
    domain = urlparse(url).netloc
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and domain in urlparse(href).netloc:
            subpage = urlparse(href).path
            subpages.add(subpage)
    
    return subpages

def get_subpage_urls(url):
    subpage_urls = set()
    domain = urlparse(url).netloc
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            absolute_url = urljoin(url, href)
            parsed = urlparse(absolute_url)
            if parsed.netloc == domain and parsed.path not in ['', '/']:
                subpage_urls.add(absolute_url)
    
    return subpage_urls


def search_google(query):
    search_url = "https://www.google.com/search?q={}".format(query)
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for link in soup.find_all('a'):
        href = link.get('href')
        # prevent urls of google.com from being returned
        if href and 'google.com' not in href and 'url?q=' in href:
                results.append(href.split('url?q=')[1].split('&sa=U')[0])
    return results


def search_google_lib(query):
    websites = []
    for website in search(query, num_results=30):
        websites.append(website)
    return websites

# search google for websites -> get email from the page -> get subpages -> get email from subpages

def get_emails_from_query(query):
    # make set of emails
    emails = set()
    # search google for websites
    websites = search_google_lib(query)
    # get emails from the page
    for website in websites:
        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'html.parser')
        emails.update(find_emails(str(soup)))
        # get subpages
        subpages = get_subpage_urls(website)
        # get emails from subpages
        for subpage in subpages:
            response = requests.get(subpage)
            soup = BeautifulSoup(response.text, 'html.parser')
            emails.update(find_emails(str(soup)))


    return emails

print(get_emails_from_query("physiotherapy singapore"))