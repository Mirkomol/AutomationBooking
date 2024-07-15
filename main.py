from automationbooking import *

# hello 
# Main Automation Class
class BookingAutomation:
    def __init__(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.booking_page = BookingPage(self.driver)
        self.payment_page = PaymentPage(self.driver)

    def run(self):
        try:
            self.booking_page.open_url("http://localhost:3000/")
            time.sleep(3)
            self.booking_page.open_url("http://localhost:3000/places/balzeAlte")

            try:

                calendar_input = self.booking_page.wait_for_element(By.CSS_SELECTOR,
                    'input[class="relative transition-all duration-300 py-2.5 pl-4 pr-14 w-full border-gray-300 dark:bg-slate-800 '
                    'dark:text-white/80 dark:border-slate-600 rounded-lg tracking-wide font-light '
                    'text-sm placeholder-gray-400 bg-white focus:ring disabled:opacity-40 disabled:cursor-not-allowed '
                    'focus:border-blue-500 focus:ring-blue-500/20"]')
                calendar_input.click()
                calendar_input.send_keys("10/07/2024 ~ 11/07/2024")
            except:
                print("Website is glitching, trying again...")

            self.booking_page.fill_booking_form("Test User", "mirkamol@extramus.eu", "mirkamol@extramus.eu","7777777777", "2", "0")
            self.booking_page.accept_terms()

            time.sleep(2)
            self.booking_page.confirm_booking()
            self.booking_page.handle_alert(action="dismiss")

            time.sleep(2)
            self.booking_page.confirm_booking()
            self.booking_page.handle_alert(action="accept")

            self.payment_page.fill_payment_details("Name", "Surname", "5256103270096532", "11", "2036", "123")
            time.sleep(2)
            self.payment_page.submit_payment()

        except Exception as e:
            print("An error occurred:", e)
        finally:
            time.sleep(30)
            self.driver.quit()

if __name__ == "__main__":
    automation = BookingAutomation()
    automation.run()
