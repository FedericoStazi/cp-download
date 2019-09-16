import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time

f = open('data.json', 'r')
data = json.loads(f.read())
f.close()

options = Options()
options.headless = True
driver = {}

options_headed = Options()
options_headed.headless = False

def close_all():
    global drive

    for url in driver:
        driver[url].close()
    driver.clear()

    print("closed all")

def limit_browsers():

    if len(driver) >3:
        close_all()

def get_elements(url, js):

    if url not in driver:
        limit_browsers()
        driver[url] = webdriver.Firefox(options=options)
        driver[url].get(url)
        print("Downloaded "+url)

    try:
        return driver[url].execute_script("return "+js)
    except:
        print("exception")
        close_all()
        time.sleep(20)
        return get_elements(url, js)
        driver_headed = webdriver.Firefox(options=options_headed)
        driver_headed[url].get(url)
        driver_headed.close()
        return driver[url].execute_script("return "+js)

def max_page(params, username):
    if params["url"]:
        url = params["url"].replace("__username__", username)
        return get_elements(url, params["js"]["max_page"]) #gets the number of pages
    else:
        return "1"

def submissions_per_page(params, username, page_id):

    if params["page_one_url"] and page_id == "1":
        url = params["page_one_url"].replace("__username__", username)
    else:
        url = params["url"].replace("__username__", username).replace("__page_id__", page_id)

    js = params["js"]
    v = []
    elements_number = int(get_elements(url, js["get_elements_number"]))

    for i in range(elements_number):

        v.append({\
            "id": get_elements(url, js["id"].replace("__element__", str(i))),\
            "time": get_elements(url, js["time"].replace("__element__", str(i))),\
            "solved": get_elements(url, js["solved"].replace("__element__", str(i)))\
        })

    return v #gets id, time, solved of all the submissions on a page

def solved_problems(params, username):

    url = params["url"].replace("__username__", username)
    js = params["js"]
    v = []
    elements_number = int(get_elements(url, js["get_elements_number"]))

    for i in range(elements_number):
        v.append(get_elements(url, js["id"].replace("__element__", str(i))))

    return v #gets ids of solved problem

def all_submissions(source, username, max_page):

    if source["solved_problems"]["url"]:
        page_ids = solved_problems(source["solved_problems"], username)
    else:
        page_ids = range(1, int(max_page)+1)

    params=source["submissions_per_page"]
    v = []
    for page_id in page_ids:
        v.extend(submissions_per_page(params, username, str(page_id)))
    return v

for source_name in data["sources"]:

    source = data["sources"][source_name]
    username = source["username"]

    l = all_submissions(source, username, max_page(source["max_page"], username))
    for x in l:
        print(x)

    exit(0)
