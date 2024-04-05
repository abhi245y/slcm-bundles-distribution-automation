
from selenium import webdriver
import yaml
import json
import requests
import time
import pprint
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get("https://examerp.keralauniversity.ac.in/")

with open('./configs/cookies.json', "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    driver.add_cookie(cookie)


driver.get("https://examerp.keralauniversity.ac.in/user/dashboard")

script = '''
return (async () => {
  const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/qpcode-wise-bundle-list", {
    "headers": {
      "accept": "application/json",
      "content-type": "application/json",
      "x-csrftoken": ""
    },
    "body": '{"qp_code":"R 7558"}',
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
  });
  const data = await response.json();
  return data;
})();
'''

script2 = '''
return (async () => {
  const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/campwise-bundle-list?format=json", {
    "headers": {
       "accept": "application/json, text/javascript, */*; q=0.01",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "x-csrftoken": ""
    },
    "body": "qp_code=R+7558",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
  });
  const data = await response.json();
  return data;
})();
'''
# data = driver.execute_script (script)
data2 =  driver.execute_script (script2)
# pprint.pprint(data)
pprint.pprint(data2)
