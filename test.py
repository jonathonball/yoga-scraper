from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get('https://nationalyogaacademy.com/schedule/')
assert "Schedule" in driver.title
try:
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "bw-calendar-container")))
finally:
    driver.quit()

day = driver.find_element(By.CSS_SELECTOR, "span[data-bw-startdate='2020-02-05'")

# The element I'm trying to select is a span with a data attribute
# span[data-bw-startdate="2020-02-05"]
day.click()

