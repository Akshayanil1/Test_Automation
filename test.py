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
time.sleep(3)  # Sleep to allow page to load

# 3. Log in with test credentials
username = driver.find_element(By.ID, "user-name")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "login-button")

username.send_keys("standard_user")  # Username
password.send_keys("secret_sauce")  # Password
login_button.click()  # Log in
time.sleep(3)  # Sleep to allow login action to complete

# 4. Wait until the product grid is visible
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))  # Wait until products load
time.sleep(2)  # Sleep to allow products to load completely

# 5. Add 5 random items to the cart
added_items = 0
while added_items < 5:  # Ensure exactly 5 items are added
    items = driver.find_elements(By.XPATH, "//button[contains(@class, 'btn_inventory')]")  # Re-fetch the list of "Add to Cart" buttons
    available_items = [item for item in items if item.is_displayed() and item.is_enabled()]  # Filter out disabled items
    
    if available_items:
        random_item = random.choice(available_items)  # Select a random available item
        random_item.click()
        added_items += 1
        print(f"Added item {added_items}")
        time.sleep(5)  # Sleep for 5 seconds after adding each item
    else:
        print("No available items to add.")
        break

# 6. Wait for the cart icon to update
time.sleep(2)

# 7. Click on the cart icon to verify the items were added
cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
cart_icon.click()
time.sleep(2)  # Sleep to allow cart page to load

# 8. Wait for the cart page to load
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_list")))
time.sleep(2)  # Sleep to ensure page is fully loaded

# 9. Click the "Checkout" button to proceed to checkout
checkout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Checkout')]")
checkout_button.click()
time.sleep(3)  # Sleep to allow checkout page to load

# 10. Enter checkout information (First name, Last name, ZIP code)
first_name = driver.find_element(By.ID, "first-name")
last_name = driver.find_element(By.ID, "last-name")
zip_code = driver.find_element(By.ID, "postal-code")

first_name.send_keys("John")
last_name.send_keys("Smith")
zip_code.send_keys("787878")
time.sleep(5)  # Sleep for 5 seconds after entering name and postal code

# 11. Click the "Continue" button
continue_button = driver.find_element(By.XPATH, "//input[@value='Continue']")
continue_button.click()
time.sleep(3)  # Sleep to ensure the continue button is clicked and the next page loads

# 12. Wait for the checkout page to load (Make sure it's fully loaded before looking for the total price)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label")))
time.sleep(2)  # Sleep to ensure page is fully loaded

# 13. Get and print the total price from the checkout page
try:
    total_price = driver.find_element(By.CLASS_NAME, "summary_total_label")  # Use a more reliable class name if XPath fails
    print("Total Price:", total_price.text)
except Exception as e:
    print("Error retrieving total price:", e)

# 14. Click the "Finish" button to complete the checkout
finish_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Finish')]")
finish_button.click()
time.sleep(3)  # Sleep to ensure the finish button click is processed

# 15. Wait for the confirmation page to load
time.sleep(3)  # Sleep to allow the confirmation page to load

# 16. Close the browser
driver.quit()
