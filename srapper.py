import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  

# Define the download directory inside the main directory
main_dir = os.path.join(os.getcwd(), "csv")  # Creates 'csv' folder in the current working directory

# Ensure the download directory exists
os.makedirs(main_dir, exist_ok=True)

# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless=new")  # Enable headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920,1080")  # Set window size
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": main_dir,  # Set default download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,  # Ensure the directory is created if not exists
    "safebrowsing.enabled": True  # Enable safe browsing
})

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

def is_file_downloaded(directory, filename, wait_time=30):
    """
    Check if the file is downloaded within the specified wait time.
    """
    end_time = time.time() + wait_time
    while time.time() < end_time:
        if filename in os.listdir(directory):
            return True
        time.sleep(1)
    return False

def rename_file_with_date(directory, filename):
    """
    Rename the downloaded file by appending the current date to its name.
    """
    today_date = datetime.today().strftime('%Y%m%d')
    new_filename = f"{filename.split('.')[0]}_{today_date}.{filename.split('.')[1]}"
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
    return new_filename

def is_today_data_downloaded(directory):
    """
    Check if today's data has already been downloaded.
    """
    today_date = datetime.today().strftime('%Y%m%d')
    for filename in os.listdir(directory):
        if today_date in filename:
            return True
    return False

try:
    # Check if today's data has already been downloaded
    if is_today_data_downloaded(main_dir):
        print("Today's data has already been downloaded.")
    else:
        # Navigate to the login page
        driver.get("https://propfinder.app/login")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "email")))

        # Locate the email and password fields
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        
        # Enter your credentials
        email_field.send_keys(os.getenv("PROPFINDER_USERNAME"))
        password_field.send_keys(os.getenv("PROPFINDER_PASSWORD"))

        # Submit the login form
        password_field.send_keys(Keys.RETURN)

        # Wait for navigation to the NBA data page
        WebDriverWait(driver, 50).until(EC.url_to_be("https://propfinder.app/nba"))

        # Navigate to the NBA data page
        driver.get("https://propfinder.app/nba")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Export']")))

        # Locate and click the export button
        export_button = driver.find_element(By.XPATH, "//button[@aria-label='Export']")
        export_button.click()

        # Wait for the download options to appear and click 'Download as CSV'
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Download as CSV')]")))
        download_csv_option = driver.find_element(By.XPATH, "//li[contains(text(), 'Download as CSV')]")
        download_csv_option.click()

        # Define the expected filename (adjust based on actual filename)
        expected_filename = "PropFinder.csv"

        # Wait for the file to be downloaded
        if is_file_downloaded(main_dir, expected_filename):
            print(f"File '{expected_filename}' has been downloaded successfully.")
            
            # Rename the file with the current date
            new_filename = rename_file_with_date(main_dir, expected_filename)
            print(f"File has been renamed to '{new_filename}'")
        else:
            print(f"File '{expected_filename}' was not downloaded within the expected time.")

finally:
    # Close the browser
    driver.quit()
