#!/usr/bin/env python3
"""
Scrape schedules from yoga studio websites. Print aggregated report.
"""
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def national_yoga_academy(driver, wait, site_key, target_date, results):
    """
    home sweet home
    """
    driver.get('https://nationalyogaacademy.com/schedule/')
    assert "Schedule" in driver.title

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bw-calendar")))
    driver.find_element(By.CSS_SELECTOR, "span[data-bw-startdate='" + target_date + "'").click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "date-" + target_date)))
    days = driver.find_elements(By.CLASS_NAME, "bw-session__info")
    results[site_key] = []
    for day in days:
        results[site_key].append({
            "start": day.find_element(By.CLASS_NAME, "hc_starttime").text,
            "end": day.find_element(By.CLASS_NAME, "hc_endtime").text,
            "name": day.find_element(By.CLASS_NAME, "bw-session__name").text
        })

###################
OPTIONS = Options()
OPTIONS.add_argument('-headless')
DRIVER = webdriver.Firefox(options=OPTIONS)
WAIT = WebDriverWait(DRIVER, 10)
TARGET = '2020-02-07'
RESULTS = {}
JOBS = [
    {'key': 'national_yoga_academy'},
]
for job in JOBS:
    job_key = job['key']
    try:
        locals()[job_key](DRIVER, WAIT, job_key, TARGET, RESULTS)
    except Exception:
        print(str(Exception), file=sys.stderr)
print(json.dumps(RESULTS))
DRIVER.quit()
