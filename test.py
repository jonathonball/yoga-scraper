#!/usr/bin/env python3
"""
Scrape schedules from yoga studio websites. Print aggregated report.
"""
import sys
import json
import argparse
import datetime
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

def hot_house_yoga(driver, wait, site_key, target_date, results):
    """
    large schedule
    """
    day_of_week = datetime.datetime.strptime(target_date,'%Y-%m-%d').strftime('%w')
    driver.get('https://hothouseyogi.com/schedule/')
    assert "Schedule" in driver.title

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.hc_time')))
    classes = driver.find_elements(By.CSS_SELECTOR, "tr.hc_class[data-hc-day='" + day_of_week + "']")
    results[site_key] = []
    for row in classes:
        results[site_key].append({
            "start": row.find_element(By.CLASS_NAME, "hc_starttime").text,
            "end": row.find_element(By.CLASS_NAME, "hc_endtime").text,
            "name": row.find_element(By.CSS_SELECTOR, ".classname > a").text[2:],
        })

###################
PARSER = argparse.ArgumentParser(description="Scrape schedules from yoga studio websites")
PARSER.add_argument('--noheadless', action='store_true')
PARSER.add_argument('--nodetach', action='store_true')
ARGS = PARSER.parse_args()
OPTIONS = Options()
if not ARGS.noheadless:
    OPTIONS.add_argument('-headless')
DRIVER = webdriver.Firefox(options=OPTIONS)
WAIT = WebDriverWait(DRIVER, 10)
TARGET = '2020-02-07'
RESULTS = {}
JOBS = [
    {'key': 'national_yoga_academy'},
    {'key': 'hot_house_yoga'}
]
for job in JOBS:
    job_key = job['key']
    try:
        locals()[job_key](DRIVER, WAIT, job_key, TARGET, RESULTS)
    except Exception as exception:
        print(type(exception), file=sys.stderr)
        print(exception.args, file=sys.stderr)
        print(exception, file=sys.stderr)
print(json.dumps(RESULTS))
if not ARGS.nodetach:
    DRIVER.quit()
