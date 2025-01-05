import time

import urllib3.exceptions
from selenium.webdriver.support.wait import WebDriverWait
import requests
import os

def translate_text(txt, src, dst):
    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/html"

    payload = {
        "from": src,
        "to": dst,
        "html": txt
    }
    headers = {
        "x-rapidapi-key": "e7e3ae7af0msh96d824e7ea140d0p1bde70jsn9f0f4c0df6a0",
        "x-rapidapi-host": "google-translate113.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()['trans']

def word_histo(words):
    word_count = dict()
    for word in words.strip().lower().split(" "):
        word_count[word] = word_count.get(word,0) + 1
    return word_count

def download_file(url, title, folder):
    path = os.path.abspath(os.path.join(".", folder))
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = title[:10].replace(" ", "_") + "_" + str(time.time_ns()) + ".png"
    file_path = os.path.join(path, file_name)

    # time being retry for 3 times; can be improved with retry decorators later
    for i in range(3):
        try:
            res = requests.get(url)
            if res.ok:
                with open(file_path, "wb") as f:
                    f.write(res.content)
            return file_name
        except urllib3.exceptions.ReadTimeoutError:
            continue

def add_driver_wait(driver, timeout):
    return WebDriverWait(driver, timeout)
