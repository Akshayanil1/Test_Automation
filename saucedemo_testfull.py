from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# 1. Setup WebDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service)

# 2. Open the Saucedemo login page
driver.get("https://www.saucedemo.com/")
time.sleep(3)

# 3. Log in with test credentials
username = driver.find_element(By.ID, "user-name")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "login-button")

username.send_keys("standard_user")
password.send_keys("secret_sauce")
login_button.click()
time.sleep(3)

# 4. Wait until the product grid is visible
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
time.sleep(2)

# 5. Add a random number of items (between 1 and the total available items) to the cart
buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'btn_inventory')]")
available_items = len(buttons)
print(f"Total items available: {available_items}")

# Generate a random number of items to add
items_to_add = random.randint(1, available_items)
print(f"Randomly selected {items_to_add} items to add to the cart.")

added_items = 0
for button in buttons:
    if button.text.strip().upper() == "ADD TO CART":
        button.click()
        added_items += 1
        print(f"Added item {added_items}.")
        time.sleep(3)  # Wait after each addition

        # Stop if the required number of items is added
        if added_items >= items_to_add:
            break

# 6. Click on the cart icon to verify items
cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
cart_icon.click()
time.sleep(3)

# 7. Proceed to checkout
checkout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Checkout')]")
checkout_button.click()
time.sleep(3)

# 8. Fill in checkout details
first_name = driver.find_element(By.ID, "first-name")
last_name = driver.find_element(By.ID, "last-name")
zip_code = driver.find_element(By.ID, "postal-code")

first_name.send_keys("John")
last_name.send_keys("Smith")
zip_code.send_keys("787878")
time.sleep(5)

# 9. Click "Continue"
continue_button = driver.find_element(By.XPATH, "//input[@value='Continue']")
continue_button.click()
time.sleep(3)

# 10. Retrieve and print the total price
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label")))
total_price = driver.find_element(By.CLASS_NAME, "summary_total_label").text
print(f"Total Price: {total_price}")

# 11. Finish checkout
finish_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Finish')]")
finish_button.click()
time.sleep(3)

# 12. Close the browser
driver.quit()
