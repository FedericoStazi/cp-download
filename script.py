import json
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

SLEEP_TIME = 3

f = open('data.json', 'r')
data = json.loads(f.read())
f.close()

options = Options()
options.headless = True
driver = {}

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
        if len(driver):
            close_all()
        driver[url] = webdriver.Firefox(options=options)
        driver[url].get(url)
        print("downloaded "+url)

    try:
        return driver[url].execute_script(js)
    except:
        print("exception")
        close_all()
        time.sleep(SLEEP_TIME)
        return get_elements(url, js)

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
            "name": get_elements(url, js["name"].replace("__element__", str(i))),\
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

def all_submissions(params, username, max_page):

    if source["solved_problems"]["url"]:
        page_ids = solved_problems(source["solved_problems"], username)
    else:
        page_ids = range(1, int(max_page)+1)

    params=source["submissions_per_page"]
    v = []
    for page_id in page_ids:
        v.extend(submissions_per_page(params, username, str(page_id)))
    return v

def good_submissions(submissions):

    for x in submissions:
        print(x)

    taken = {}
    v = []
    for s in submissions:
        if s["solved"] and s["name"] not in taken:
            taken[s["name"]] = True
            v.append(s)

    return v

def code(params, problem, username):

    url = params["url"].replace("__problem_id__", problem["id"]).replace("__username__", username)
    js = params["js"]
    lines_number = int(get_elements(url, js["lines_number"]))
    code_lines = []

    for i in range(lines_number):
        code_lines.append(get_elements(url, js["line"].replace("__element__", str(i))))

    return {\
        "name": problem["name"]+get_elements(url, js["extension"]),\
        "code": ("\n").join(code_lines)\
    }

def all_codes(params, problems, folder):

    folder = os.path.expanduser(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)

    for p in problems:
        x = code(params, p, username)
        file = open(folder+"/"+x["name"], "w")
        file.write(x["code"])
        file.close()

    close_all()

for source_name in data["sources"]:

    source = data["sources"][source_name]
    username = source["username"]
    folder = data["folder"]

    if username == "":
        continue

    all_codes(source["code"], good_submissions(all_submissions(source, username, max_page(source["max_page"], username))), folder+source_name)
