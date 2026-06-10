import pytest
import time
from helium import start_chrome, click, S, go_to, get_driver, wait_until, alert_is_present, accept_alert

BASE_URL = 'https://www.demoblaze.com'

def test_tc_ui_01_homepage_loads(browser_context):
    start_chrome(BASE_URL)
    driver = get_driver()
    assert 'STORE' in driver.title
    assert S('.navbar-brand').exists()
    assert S('.card-title').exists()
    driver.save_screenshot('report/tc_ui_01.png')

def test_tc_ui_02_successful_login(browser_context):
    start_chrome(BASE_URL)
    click(S('#login2'))
    wait_until(S('#loginusername').exists)
    S('#loginusername').web_element.send_keys('testuser1')
    S('#loginpassword').web_element.send_keys('Test1234!')
    click('Log in')
    wait_until(S('#logout2').exists)
    driver = get_driver()
    assert S('#logout2').web_element.is_displayed()
    driver.save_screenshot('report/tc_ui_02.png')

def test_tc_ui_03_login_wrong_password(browser_context):
    start_chrome(BASE_URL)
    click(S('#login2'))
    wait_until(S('#loginusername').exists)
    S('#loginusername').web_element.send_keys('testuser1')
    S('#loginpassword').web_element.send_keys('wrongpassword')
    click('Log in')
    wait_until(alert_is_present)
    driver = get_driver()
    alert_text = driver.switch_to.alert.text
    accept_alert()
    assert len(alert_text) > 0
    assert not S('#logout2').exists()
    driver.save_screenshot('report/tc_ui_03.png')

def test_tc_ui_04_add_to_cart(browser_context):
    start_chrome(BASE_URL)
    wait_until(S('.card-title').exists)
    click(S('.card-title'))
    wait_until(S('//a[text()="Add to cart"]').exists)
    click('Add to cart')
    wait_until(alert_is_present)
    driver = get_driver()
    alert_text = driver.switch_to.alert.text
    assert 'added' in alert_text.lower()
    accept_alert()
    driver.save_screenshot('report/tc_ui_04.png')

def test_tc_ui_05_category_filter(browser_context):
    start_chrome(BASE_URL)
    wait_until(S('.card-title').exists)
    items_before = len(S('.card-title').web_element.find_elements_by_class_name('card-title')) if hasattr(S('.card-title').web_element, 'find_elements_by_class_name') else 9
    click('Phones')
    time.sleep(2)
    driver = get_driver()
    items_after = len(driver.find_elements_by_class_name('card-title'))
    assert items_after > 0
    assert items_after <= items_before
    driver.save_screenshot('report/tc_ui_05.png')