# cp-download
Scipt used to automatically download a user's submissions to the most famous competitive programming websites.

## Installing

This script is written using *Python 3.6* and needs the *Selenium* library.

```
   sudo apt-get install python3
   pip3 install selenium
```

Selenium needs *Geckodriver 0.25.0* to run an headless Firefox browser

```
   wget https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz
   tar -C /usr/bin -zxvf geckodriver-v0.25.0-linux64.tar.gz
   
```
## Websites

These are the websites supported by cp-download:

##### Ready

- codeforces
- codechef

#### Work in progress

- oj.uz
- sphere
- wcipeg
- acm.timus.ru
- onlinejudge.org
- judge.u-aizu.ac.jp


## Simple usage

The user.json file contains your informations. Next to the *folder* field you should choose the folder where you want your files to be saved. In the other fields you should write your username in the websites. If you don't have an account in some of those websites, you can leave the field empty. Here's an example of a correct user.json file:

```
{
    "folder": "~/competitive-programming/",
    "codeforces": "FedericoS",
    "codechef": "federico_s",
    ...

```

You will now be able to run the script. To do so open a terminal in the folder where you downloaded all the files, and type:
```
python3 script.py
```

## Adding websites

**Be careful! If you only want to download your submissions, you do NOT have to read this section. You should read it only if you are interested in how the script works or if you want to add a website that is not currently included**

TODO general description (maybe in its own section)

If you want to download submissions from a website that isn't in the list, you can add it in the user.json file and in the data.json file. Here's a brief description of how the script works, which will allow you to download submissions from other websites.

TODO TYPES

TODO KEYWORDS

In the *data.json* file, *sources* contains an entry for each competitive programming website. This is the structure of a sample entry:

* ##### max_page
   If the submissions of a user or are listed in multiple pages, *max_page* gets the number of pages.
   * ##### url
      The url where the maximum page can be found.
   * ##### js
      This entry contains the javascript functions that get the value you are looking for from the page.
      * ##### max_page
         Returns the max page. If all the submissions are on a page, just write "return 1".
      
* ##### solved_problems
   If all the submissions of a user or are listed together, leave the *url* field blank so that this part will be ignored.
   If each problem has its own submissions page, this part is used to get the ids of the solved problems.
   * ##### url
      The url where the ids of the solved problems can be found.
   * ##### page_one_url
      NOT ADDED YET
   * ##### js
      This entry contains the javascript functions that get the values you are looking for from the page.
      * ##### get_elements_number
         Returns the number of solved problems on the page.
      * ##### id
         Gets the id of the *__element*-th problem.
         
* ##### submissions_per_page
   This part gets all the submission's ids on a page. ...
   * ##### url
      The url where the ids of the submissions can be found. Use *__page_number* in the url if there are multiple pages. 
   * ##### page_one_url
      Sometimes the first page of submissions is different from the other pages. Write the url of the first page here.
   * ##### js
      This entry contains the javascript functions that get the values you are looking for from the page.
      * ##### get_elements_number
         Returns the number of submissions on the page.
      * ##### id
         Gets the id of the *__element*-th submission.
      * ##### name
         Gets the name of the *__element*-th submission. This is the name of the file where the solution is saved.
      * ##### time
         Gets the submission time of the *__element*-th submission. This field is not currently used. You can therefore simply write "return 0".
      * ##### solved
         This field can be true or false. It is true if the *__element*-th submission solves the problem, false otherwise.
         
* ##### code
   This part downloads the code of the solution.
   * ##### url
      The url where the code of the submission can be found.
   * ##### js
      This entry contains the javascript functions that get the values you are looking for from the page.
      * ##### lines_number
         Returns the number of lines of code in the submission.
      * ##### id
         Gets the *__element*-th line of the submission.
      * ##### extension
         Gets the extension of the file where the submission is saved.
         

## Future features

- adding missing websites
- adding feature that stops the script from downloading already downloaded files
- adding extension detection in codeforces and codechef

## Contributing

If you successfully add a website that isn't in the list, please make a pull request!

## Author

* **Federico Stazi** - [FedericoStazi](https://github.com/FedericoStazi)
