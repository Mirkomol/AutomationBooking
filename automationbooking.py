import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Base class for common WebDriver setup and teardown
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))

    def click_element(self, by, value, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
        element.click()
        return element

    def fill_input_field(self, by, value, text, timeout=10):
        element = self.wait_for_element(by, value, timeout)
        element.send_keys(text)
        return element

    def select_dropdown(self, by, value, text, timeout=10):
        select_element = Select(self.wait_for_element(by, value, timeout))
        select_element.select_by_visible_text(text)
        return select_element

# Derived class for specific page interactions
class BookingPage(BasePage):
    def fill_booking_form(self, fullname, email, phone, no_of_adults, no_of_babies):
        self.fill_input_field(By.NAME, "fullname", fullname)
        self.fill_input_field(By.NAME, "email", email)
        self.fill_input_field(By.NAME, "phone_num", phone)
        self.select_dropdown(By.NAME, "no_of_adults", no_of_adults)
        self.select_dropdown(By.NAME, "no_of_babies", no_of_babies)

    def accept_terms(self):
        self.click_element(By.NAME, "terms")

    def confirm_booking(self):
        self.click_element(By.XPATH, "//div[contains(text(), 'Conferma prenotazione')]")

    def handle_alert(self, action="accept"):
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print("Alert text:", alert.text)
            if action == "accept":
                alert.accept()
            else:
                alert.dismiss()
        except:
            print("No alert found")


# Derived class for handling payment
class PaymentPage(BasePage):
    def fill_payment_details(self, first_name, last_name, card_number, exp_month, exp_year, cvv):
        self.fill_input_field(By.NAME, "ACCNTFIRSTNAME", first_name)
        self.fill_input_field(By.NAME, "ACCNTLASTNAME", last_name)
        self.fill_input_field(By.NAME, "PAN", card_number)
        self.select_dropdown(By.NAME, "EXPDT_MM", exp_month)
        self.select_dropdown(By.NAME, "EXPDT_YY", exp_year)
        self.fill_input_field(By.NAME, "CVV", cvv)

    def submit_payment(self):
        self.click_element(By.ID, "continue")
        self.click_element(By.ID, "confirm")


