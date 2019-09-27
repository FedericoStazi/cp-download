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

## Adding websites

If you want to download submissions from a website that isn't in the list, you can add it in the user.json file and in the data.json file. Here's a brief description of how the script works, which will allow you to download submissions from other websites.

**TODO**

## Future features

- adding missing websites
- adding feature that stops the script from downloading already downloaded files

## Contributing

If you successfully add a website that isn't in the list, please make a pull request!

## Author

* **Federico Stazi** - [FedericoStazi](https://github.com/FedericoStazi)
