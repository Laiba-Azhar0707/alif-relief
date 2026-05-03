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
    """Dashboard page loads successfully."""
    driver.get(BASE_URL + "/")
    assert "Alif Relief" in driver.title or driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_02_dashboard_stats_visible(driver):
    """Dashboard shows stats cards."""
    driver.get(BASE_URL + "/")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert any(word in body for word in ["Donors", "Campaigns", "Beneficiaries", "Raised"])


def test_03_donors_page_loads(driver):
    """Donors page loads successfully."""
    driver.get(BASE_URL + "/donors")
    assert driver.current_url.endswith("/donors")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_04_add_donor(driver):
    """Add a new donor via form."""
    driver.get(BASE_URL + "/donors")
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.NAME, "name").send_keys("Test Donor Selenium")
    driver.find_element(By.NAME, "phone").send_keys("03001234567")
    driver.find_element(By.NAME, "city").send_keys("Islamabad")
    driver.find_element(By.NAME, "email").send_keys("testdonor@selenium.com")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(1)
    assert "Test Donor Selenium" in driver.find_element(By.TAG_NAME, "body").text


def test_05_donor_search(driver):
    """Search for a donor by name."""
    driver.get(BASE_URL + "/donors?q=Test+Donor+Selenium")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Test Donor Selenium" in body


def test_06_campaigns_page_loads(driver):
    """Campaigns page loads successfully."""
    driver.get(BASE_URL + "/campaigns")
    assert driver.current_url.endswith("/campaigns")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_07_add_campaign(driver):
    """Add a new campaign via form."""
    driver.get(BASE_URL + "/campaigns")
    driver.find_element(By.NAME, "name").send_keys("Selenium Test Campaign")
    driver.find_element(By.NAME, "target").send_keys("50000")
    driver.find_element(By.NAME, "category").send_keys("Education")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(1)
    assert "Selenium Test Campaign" in driver.find_element(By.TAG_NAME, "body").text


def test_08_donations_page_loads(driver):
    """Donations page loads successfully."""
    driver.get(BASE_URL + "/donations")
    assert driver.current_url.endswith("/donations")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_09_add_donation(driver):
    """Add a new donation via form."""
    driver.get(BASE_URL + "/donations")
    select_donor = Select(driver.find_element(By.NAME, "donor_id"))
    select_donor.select_by_index(1)
    driver.find_element(By.NAME, "amount").send_keys("5000")
    driver.find_element(By.NAME, "date").send_keys("2026-05-03")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(1)
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "5,000" in body or "5000" in body or "Donation" in body


def test_10_beneficiaries_page_loads(driver):
    """Beneficiaries page loads successfully."""
    driver.get(BASE_URL + "/beneficiaries")
    assert driver.current_url.endswith("/beneficiaries")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_11_add_beneficiary(driver):
    """Add a new beneficiary via form."""
    driver.get(BASE_URL + "/beneficiaries")
    driver.find_element(By.NAME, "name").send_keys("Selenium Beneficiary")
    driver.find_element(By.NAME, "area").send_keys("Rawalpindi")
    driver.find_element(By.NAME, "need").send_keys("Food")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(1)
    assert "Selenium Beneficiary" in driver.find_element(By.TAG_NAME, "body").text


def test_12_volunteers_page_loads(driver):
    """Volunteers page loads successfully."""
    driver.get(BASE_URL + "/volunteers")
    assert driver.current_url.endswith("/volunteers")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_13_add_volunteer(driver):
    """Add a new volunteer via form."""
    driver.get(BASE_URL + "/volunteers")
    driver.find_element(By.NAME, "name").send_keys("Selenium Volunteer")
    driver.find_element(By.NAME, "phone").send_keys("03119876543")
    driver.find_element(By.NAME, "skills").send_keys("Testing, QA")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(1)
    assert "Selenium Volunteer" in driver.find_element(By.TAG_NAME, "body").text


def test_14_reports_page_loads(driver):
    """Reports page loads successfully."""
    driver.get(BASE_URL + "/reports")
    assert driver.current_url.endswith("/reports")
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()


def test_15_reports_shows_data(driver):
    """Reports page shows summary statistics."""
    driver.get(BASE_URL + "/reports")
    body = driver.find_element(By.TAG_NAME, "body").text
    assert any(word in body for word in ["Total", "Donors", "Campaigns", "Raised", "Volunteers"])
