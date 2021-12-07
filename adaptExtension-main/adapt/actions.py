
from selenium import webdriver
import time
from .constants import CHROMEDRIVER_LOCATION, ADAPT_EXTENSION_LOCATION,  \
    ADAPT_EMAIL, ADAPT_PASSWORD,BINARY_LOCATION
from .googlesheet_operations import sheet_data, getLinkedinCookies, upadteEmail


def chrome_driver(cookies):
    driver_location = CHROMEDRIVER_LOCATION
    binary_location = BINARY_LOCATION

    options = webdriver.ChromeOptions()
    options.add_extension(ADAPT_EXTENSION_LOCATION)
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = binary_location
    web_driver = webdriver.Chrome(executable_path=driver_location, chrome_options=options)
    web_driver.maximize_window()
    web_driver.implicitly_wait(5)

    web_driver.get("https://www.linkedin.com")
    for cookie in cookies:
        web_driver.add_cookie(cookie)

    web_driver.get("https://www.linkedin.com")
    return web_driver


def getEmail(linkedin_url, driver, i):
    email = 'Not Found'
    driver.switch_to_window(driver.window_handles[i])
    driver.get(linkedin_url)
    driver.execute_script("window.open('https://prospector.adapt.io/single?undefined', 'new_window')")
    # print(driver.window_handles)
    i += 1
    driver.switch_to_window(driver.window_handles[1])
    try:
        driver.find_element_by_class_name("anchor-link").click()
        userEmail = driver.find_element_by_id("userEmail")
        userPassword = driver.find_element_by_id("userPassword")
        userEmail.send_keys(ADAPT_EMAIL)
        userPassword.send_keys(ADAPT_PASSWORD)
        driver.find_element_by_class_name('action-btn').click()

    except:
        pass
    try:
        driver.find_element_by_class_name('fn-12').click()
    except:
        pass

    time.sleep(5)
    isScrapped = True
    i -= 1
    try:
        emailElem = driver.find_element_by_css_selector("span.cursor.email-address.noselect")
        email = emailElem.text
    except:
        pass
    return email


def getLinkedinData(sheet, tab):
    i = 0;
    cookies, account_name = getLinkedinCookies()
    driver = chrome_driver(cookies)
    data, sheet = sheet_data(sheet, tab)
    for each in data:
        if each['Email'] == 'Not Found' or each['Email'] == 'Catch-All':
            if each['Adapt Email'] == '':
                email = getEmail(each['LinkedIn'], driver, i)
                print(email)
                print('***********')
                upadteEmail(sheet, email, each['LinkedIn'])
            # if email != "":
            #     print(email)
