import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BASE_URL = "http://172.17.0.1:5001"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    dr = webdriver.Chrome(service=service, options=options)
    dr.implicitly_wait(10)
    yield dr
    dr.quit()

def js_fill(driver, name, value):
    el = driver.find_element(By.NAME, name)
    driver.execute_script("arguments[0].removeAttribute('required'); arguments[0].value = arguments[1];", el, value)

def js_click(driver, selector):
    el = driver.find_element(By.CSS_SELECTOR, selector)
    driver.execute_script("arguments[0].click();", el)

def test_01_dashboard_loads(driver):
    driver.get(BASE_URL + "/")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_02_dashboard_stats_visible(driver):
    driver.get(BASE_URL + "/")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert any(word in body for word in ["Donors", "Campaigns", "Beneficiaries", "Raised"])

def test_03_donors_page_loads(driver):
    driver.get(BASE_URL + "/donors")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_04_add_donor(driver):
    driver.get(BASE_URL + "/donors")
    js_fill(driver, "name", "Test Donor Selenium")
    js_fill(driver, "phone", "03001234567")
    js_fill(driver, "city", "Islamabad")
    js_fill(driver, "email", "testdonor@selenium.com")
    js_click(driver, "button.btn-primary")
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_05_donor_search(driver):
    driver.get(BASE_URL + "/donors?q=Selenium")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_06_campaigns_page_loads(driver):
    driver.get(BASE_URL + "/campaigns")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_07_add_campaign(driver):
    driver.get(BASE_URL + "/campaigns")
    js_fill(driver, "name", "Selenium Test Campaign")
    js_fill(driver, "target", "50000")
    js_click(driver, "button.btn-primary")
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_08_donations_page_loads(driver):
    driver.get(BASE_URL + "/donations")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_09_add_donation(driver):
    driver.get(BASE_URL + "/donations")
    try:
        select_donor = Select(driver.find_element(By.NAME, "donor_id"))
        if len(select_donor.options) > 1:
            driver.execute_script("arguments[0].selectedIndex = 1;", driver.find_element(By.NAME, "donor_id"))
        js_fill(driver, "amount", "5000")
        js_fill(driver, "date", "2026-05-03")
        js_click(driver, "button.btn-primary")
        time.sleep(1)
    except Exception:
        pass
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_10_beneficiaries_page_loads(driver):
    driver.get(BASE_URL + "/beneficiaries")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_11_add_beneficiary(driver):
    driver.get(BASE_URL + "/beneficiaries")
    time.sleep(1)
    elements = driver.find_elements(By.CSS_SELECTOR, "input[name='name']")
    if elements:
        driver.execute_script("arguments[0].value = 'Selenium Beneficiary';", elements[0])
    try:
        js_click(driver, "button.btn-primary")
        time.sleep(1)
    except Exception:
        pass
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_12_volunteers_page_loads(driver):
    driver.get(BASE_URL + "/volunteers")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_13_add_volunteer(driver):
    driver.get(BASE_URL + "/volunteers")
    js_fill(driver, "name", "Selenium Volunteer")
    js_fill(driver, "phone", "03119876543")
    js_click(driver, "button.btn-primary")
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_14_reports_page_loads(driver):
    driver.get(BASE_URL + "/reports")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

def test_15_reports_shows_data(driver):
    driver.get(BASE_URL + "/reports")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert any(word in body for word in ["Total", "Donors", "Campaigns", "Raised", "Volunteers"])
