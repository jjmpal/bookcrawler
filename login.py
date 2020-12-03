#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pickle
from os.path import expanduser
from configparser import ConfigParser

# Read config
config_object = ConfigParser()
config_object.read("config.ini")
logininfo = config_object["LOGININFO"]

# Open cookie file
fout = expanduser(logininfo["cookiefile"])

# Start Selenium
options = webdriver.ChromeOptions()
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(options=options)
driver.get(logininfo["url"])
time.sleep(20)

# Store cookies
pickle.dump(driver.get_cookies() , open(fout, "wb"))
