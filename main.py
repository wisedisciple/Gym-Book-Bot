from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import time

# Add your credentials at the top of your script
ACCOUNT_EMAIL = "YOUR EMAIL"  # The email you registered with
ACCOUNT_PASSWORD = "YOUR PASSWORD"      # The password you used during registration
GYM_URL = "GYM SITE URL"

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
try:
    os.mkdir(user_data_dir)
    print(f"Directory '{user_data_dir}' created successfully.")
except FileExistsError:
    print(f"Directory '{user_data_dir}' already exists.")
except OSError as e:
    print(f"Error creating directory {e}")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",value=True)
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)

driver.get(GYM_URL)

wait = WebDriverWait(driver, 6)

login_button = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
login_button.click()

email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
email_input.clear()
email_input.send_keys(ACCOUNT_EMAIL)

password_input = driver.find_element(By.NAME, value="password")
password_input.clear()
password_input.send_keys(ACCOUNT_PASSWORD)

submit_button = driver.find_element(By.ID, value="submit-button")
submit_button.click()

wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))
class_cards = driver.find_elements(By.CLASS_NAME, "ClassCard_card__KpCx5")

booked_count = 0
waitlist_count = 0
already_booked_count = 0
processed_classes = []

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME,"h2").text

    if "Tue" in day_title or "Thu" in day_title:
        text_time = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in text_time:
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
            class_info = f"{class_name} on {day_title}"

            if button.text == "Booked":
                print(f"/ Already booked: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Booked] {class_info}")
            elif button.text == "Waitlisted":
                print(f"/ Already waitlist: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Waitlisted] {class_info}")
            elif button.text == "Book Class":
                button.click()
                print(f"/ Booked: {class_name} on {day_title}")
                booked_count += 1
                processed_classes.append(f"[New Booking] {class_info}")
                time.sleep(0.5)
            elif button.text == "Join Waitlist":
                button.click()
                print(f"/ Joined waitlist for: {class_name} on {day_title}")
                waitlist_count += 1
                processed_classes.append(f"[New Waitlist] {class_info}")
                time.sleep(0.5)


## Summary

# print("\n--- BOOKING SUMMARY ---")
# print(f"Classes booked: {booked_count}")
# print(f"Waitlists joined: {waitlist_count}")
# print(f"Already booked/waitlisted: {already_booked_count}")
# print(f"Total Tuesday & Thursday 6pm classes: {booked_count + waitlist_count + already_booked_count}")
#
# print("\n--- DETAILED CLASS LIST ---")
# for class_detail in processed_classes:
#     print(f" * {class_detail}")


##Verify count

# total_booked = already_booked_count + booked_count + waitlist_count
# print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
# print(f'\n--- VERIFYING ON MY BOOKINGS PAGE')
#
# my_bookings_link = driver.find_element(By.ID, "my-bookings-link").click()
#
# wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))
#
# verified_count = 0
#
# all_cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
#
# for card in all_cards:
#     try:
#         when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
#         when_text = when_paragraph.text
#
#         if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
#             class_name = card.find_element(By.TAG_NAME, "h3").text
#             print(f" ✔ Verified: {class_name}")
#             verified_count += 1
#     except NoSuchElementException:
#         pass
#
# print(f"\n--- VERIFICATION RESULT ---")
# print(f"Expected: {total_booked} bookings")
# print(f"Found: {verified_count} bookings")
#
# if total_booked == verified_count:
#     print("✅ SUCCESS: All bookings verified!")
# else:
#     print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")


driver.quit()
