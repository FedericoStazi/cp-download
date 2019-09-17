import json
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

SLEEP_TIME = 3

options = Options()
options.headless = True
driver = {}

def close_driver():

    for i in driver:
        driver[i].close()
    driver.clear() #closes web driver

def js_run(url, js):

    if url not in driver:
        close_driver()
        driver[url] = webdriver.Firefox(options=options)
        driver[url].get(url)
        print("Downloaded: "+url)

    try:
        return driver[url].execute_script(js)
    except:
        print("Attempt failed, trying again...")
        close_driver()
        time.sleep(SLEEP_TIME)
        return js_run(url, js) #runs javascript code on an url

def params_replace(str, params):

    for p in params:
        str = str.replace(p, params[p])
    return str

def max_page(data, username):
    if data["max_page"]["url"]:
        url = params_replace(data["max_page"]["url"],{"cpd__username": username})
        return js_run(url, data["max_page"]["js"]["max_page"])
    else:
        return "1" #returns the number of pages

def solved_problems(data, username):

    url = params_replace(data["solved_problems"]["url"],{"cpd__username": username})
    js = data["solved_problems"]["js"]
    v = []
    elements_number = int(js_run(url, js["get_elements_number"]))

    for i in range(elements_number):
        v.append(js_run(url, params_replace(js["id"],{"cpd__element": str(i)})))

    return v #returns solved problem

def submissions_per_page(data, username, page_id):

    if data["submissions_per_page"]["page_one_url"] and page_id == "1":
        url = params_replace(data["submissions_per_page"]["page_one_url"],{"cpd__username": username})
    else:
        url = params_replace(data["submissions_per_page"]["url"],{"cpd__username": username, "cpd__page_id": page_id})

    js = data["submissions_per_page"]["js"]
    v = []
    elements_number = int(js_run(url, js["get_elements_number"]))

    for i in range(elements_number):

        v.append({\
            "id": js_run(url, params_replace(js["id"],{"cpd__element": str(i)})),\
            "name": js_run(url, params_replace(js["name"],{"cpd__element": str(i)})),\
            "time": js_run(url, params_replace(js["time"],{"cpd__element": str(i)})),\
            "solved": js_run(url, params_replace(js["solved"],{"cpd__element": str(i)})),\
        })

    return v #returns submissions on a page

def all_submissions(data, username, max_page):

    if data["solved_problems"]["url"]:
        page_ids = solved_problems(data, username)
    else:
        page_ids = range(1, int(max_page)+1)

    v = []
    for page_id in page_ids:
        v.extend(submissions_per_page(data, username, str(page_id)))
    return v #returns all the submissions

def good_submissions(data, username):

    taken = {}
    v = []
    submissions = all_submissions(data, username, max_page(data, username))

    for s in submissions:
        if s["solved"] and s["name"] not in taken:
            taken[s["name"]] = True
            v.append(s)

    return v #chooses the submissions

def code(data, problem, username):

    url = params_replace(data["code"]["url"],{"cpd__problem_id": problem["id"], "cpd__username": username})
    js = data["code"]["js"]
    lines_number = int(js_run(url, js["lines_number"]))
    code_lines = []

    for i in range(lines_number):
        code_lines.append(js_run(url, params_replace(js["line"],{"cpd__element": str(i)})))

    return {\
        "name": problem["name"]+js_run(url, js["extension"]),\
        "code": ("\n").join(code_lines)\
        } #returns the code of the solution

def all_codes(data, folder):

    folder = os.path.expanduser(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)

    submissions = good_submissions(data, username)

    for s in submissions:
        submission_data = code(data, s, username)
        file = open(folder+"/"+submission_data["name"], "w")
        file.write(submission_data["code"])
        file.close()

    close_driver() #saves the code of all the solutions

#main function

f = open('data.json', 'r')
json_file = json.loads(f.read())
f.close()

for source_name in json_file["sources"]:
    if source_name != "TEMPLATE":
        print(source_name+": "+json_file["sources"][source_name]["username"])

for source_name in json_file["sources"]:

    data = json_file["sources"][source_name]
    username = data["username"]
    folder = json_file["folder"]

    if username == "":
        continue

    all_codes(data, folder+source_name)
