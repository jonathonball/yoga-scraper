#!/usr/bin/env python3
"""
Scrape schedules from yoga studio websites. Print aggregated report.
"""
import sys
import json
import argparse
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from icalevents.icalevents import events

def valid_date(date):
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)

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
            "end": row.find_element(By.CLASS_NAME, "hc_endtime").text[2:],
            "name": row.find_element(By.CSS_SELECTOR, ".classname > a").text,
        })

def atma_bodha_yoga(driver, wait, site_key, target_date, results):
    """
    high intensity classes
    """
    sessions = events("http://atmabodhayoga.tulasoftware.com/calendar/feed.ics", fix_apple=True)
    results[site_key] = []
    eastern_timezone = pytz.timezone("US/Eastern")
    date_format = "%Y-%m-%d"
    time_format = date_format +" %H:%M:%S"
    for session in sessions:
        date = session.start.astimezone(eastern_timezone).strftime(date_format)
        if (date == target_date):
            results[site_key].append({
                "start": session.start.astimezone(eastern_timezone).strftime(time_format),
                "end": session.end.astimezone(eastern_timezone).strftime(time_format),
                "name": session.summary,
            })

###################
PARSER = argparse.ArgumentParser(description="Scrape schedules from yoga studio websites")
PARSER.add_argument('--noheadless', help="Prevent hiding of test browser", action='store_true')
PARSER.add_argument('--nodetach', help="Leave test browser running", action='store_true')
PARSER.add_argument('date', help="YYYY-MM-DD to search for classes", type=valid_date)
ARGS = PARSER.parse_args()
OPTIONS = Options()
if not ARGS.noheadless:
    OPTIONS.add_argument('-headless')
DRIVER = webdriver.Firefox(options=OPTIONS)
WAIT = WebDriverWait(DRIVER, 10)
RESULTS = {}
JOBS = [
    {'key': 'national_yoga_academy'},
    {'key': 'hot_house_yoga'},
    {'key': 'atma_bodha_yoga'},
]

for job in JOBS:
    job_key = job['key']
    try:
        locals()[job_key](DRIVER, WAIT, job_key, ARGS.date, RESULTS)
    except Exception as exception:
        print(type(exception), file=sys.stderr)
        print(exception.args, file=sys.stderr)
        print(exception, file=sys.stderr)
print(json.dumps(RESULTS))

if not ARGS.nodetach:
    DRIVER.quit()
