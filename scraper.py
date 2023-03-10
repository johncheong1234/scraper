import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.physiox.com.sg/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# convert to string
soup_string = str(soup)
print(soup_string)

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

# test
test_string = "My email is john.d.cheong@hotmal.com and his email is randy@gmail.com"
print(find_gmails(test_string))
print(find_emails(test_string))

print(find_emails(soup_string))
