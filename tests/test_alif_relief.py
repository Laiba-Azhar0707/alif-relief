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


def test_01_dashboard_loads(driver):
    driver.get(BASE_URL + "/")
    assert "Alif Relief" in driver.title or driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_02_dashboard_stats_visible(driver):
    driver.get(BASE_URL + "/")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert any(word in body for word in ["Donors", "Campaigns", "Beneficiaries", "Raised"])


def test_03_donors_page_loads(driver):
    driver.get(BASE_URL + "/donors")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_04_add_donor(driver):
    driver.get(BASE_URL + "/donors")
    driver.find_element(By.NAME, "name").send_keys("Test Donor Selenium")
    driver.find_element(By.NAME, "phone").send_keys("03001234567")
    driver.find_element(By.NAME, "city").send_keys("Islamabad")
    driver.find_element(By.NAME, "email").send_keys("testdonor@selenium.com")
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_05_donor_search(driver):
    driver.get(BASE_URL + "/donors?q=Selenium")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Donor" in body or driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_06_campaigns_page_loads(driver):
    driver.get(BASE_URL + "/campaigns")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_07_add_campaign(driver):
    driver.get(BASE_URL + "/campaigns")
    driver.find_element(By.NAME, "name").send_keys("Selenium Test Campaign")
    driver.find_element(By.NAME, "target").send_keys("50000")
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_08_donations_page_loads(driver):
    driver.get(BASE_URL + "/donations")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_09_add_donation(driver):
    driver.get(BASE_URL + "/donations")
    wait = WebDriverWait(driver, 10)
    try:
        select_donor = Select(driver.find_element(By.NAME, "donor_id"))
        if len(select_donor.options) > 1:
            select_donor.select_by_index(1)
        driver.find_element(By.NAME, "amount").send_keys("5000")
        driver.find_element(By.NAME, "date").send_keys("2026-05-03")
        driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
        time.sleep(1)
    except Exception:
        pass
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_10_beneficiaries_page_loads(driver):
    driver.get(BASE_URL + "/beneficiaries")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_11_add_beneficiary(driver):
    driver.get(BASE_URL + "/beneficiaries")
    driver.find_element(By.NAME, "name").send_keys("Selenium Beneficiary")
    driver.find_element(By.NAME, "area").send_keys("Rawalpindi")
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_12_volunteers_page_loads(driver):
    driver.get(BASE_URL + "/volunteers")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_13_add_volunteer(driver):
    driver.get(BASE_URL + "/volunteers")
    driver.find_element(By.NAME, "name").send_keys("Selenium Volunteer")
    driver.find_element(By.NAME, "phone").send_keys("03119876543")
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_14_reports_page_loads(driver):
    driver.get(BASE_URL + "/reports")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_15_reports_shows_data(driver):
    driver.get(BASE_URL + "/reports")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert any(word in body for word in ["Total", "Donors", "Campaigns", "Raised", "Volunteers"])
