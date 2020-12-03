#!/usr/bin/env python3
from os.path import expanduser
import os
import json
from bs4 import BeautifulSoup
import requests
import pickle
import urllib.parse
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import random
import re
from configparser import ConfigParser

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    validname = re.sub(r'(?u)[^-\w.]', '', s)
    matches = re.findall("^(\d+)\.?(.+)", validname)
    if not matches:
        return(validname)    
    else:
        i, rest = matches[0]
        return("{:04d}{}".format(int(i), rest))

# Read config
config_object = ConfigParser()
config_object.read("config.ini")
logininfo = config_object["LOGININFO"]
info = config_object["DOWNLOADINFO"]

# Make target dir and temp dir
os.makedirs(expanduser("%s/.tmp"%info["target"]), exist_ok=True)

# Start Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get(info["tocurl"])

# Load cookies
for cookie in pickle.load(open(expanduser(logininfo["cookiefile"]), "rb")):
    driver.add_cookie(cookie)

# Get toc html
driver.get(info["tocurl"])
soup = BeautifulSoup(driver.page_source, "html.parser")

# Get chapter addresses
links = {}
for anchor in soup.findAll("div", {"class": info["tocdivclass"]})[0].findAll('a'):
    if anchor.text[0].isdigit():
        outputfilename = get_valid_filename("%s.html"%anchor.text)
        links[outputfilename] = "%s%s"%(info["hostprefix"], anchor['href'])

# Randomize crawling order
items = list(links.items())
random.shuffle(items)

# Crawl chapters and store html
for name, url in items:
    outputfile = "%s/%s"%(info["target"], name)

    if os.path.isfile(outputfile):
        print("Skipping: %s"%outputfile)
        continue
        
    print(name, url)
    
    driver.get(url)
    time.sleep(10)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    region = soup.find("div", {"class": info["maindivclass"]})
    with open(outputfile, "w") as file:
        file.write(str(region))
        
    time.sleep(random.randint(2,19))

