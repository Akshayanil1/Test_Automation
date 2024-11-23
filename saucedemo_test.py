from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. Setup WebDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service)

# 2. Open the Saucedemo login page
driver.get("https://www.saucedemo.com/")

# 3. Log in with test credentials
username = driver.find_element(By.ID, "user-name")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "login-button")

username.send_keys("standard_user")  # Username
password.send_keys("secret_sauce")  # Password
login_button.click()  # Log in

# 4. Wait until the product grid is visible
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))  # Wait until products load

# 5. Click on the first product's "Add to cart" button
add_to_cart_button = driver.find_element(By.XPATH, "(//button[contains(@class, 'btn_inventory')])[1]")
add_to_cart_button.click()

# 6. Wait for the cart icon to update
time.sleep(1)

# 7. Click on the cart icon to verify the item was added
cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
cart_icon.click()

# 8. Verify that the item is in the cart by checking the page title
print("Page Title (Cart):", driver.title)

# 9. Close the browser
driver.quit()
