import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Initialize Chrome WebDriver using WebDriver Manager
from webdriver_manager.chrome import ChromeDriverManager  # Initialize Chrome WebDriver
from selenium.webdriver.chrome.service import Service    # Initialize Chrome WebDriver with Service

# Path to your Twitter links file
input_file_path = 'C:/Users/haidar/OneDrive/Desktop/Twitter Scraping/twitter_links.csv'

# Path to your Chrome driver
driver_path = "C:/Users/haidar/OneDrive/Desktop/Twitter Scraping/chromedriver.exe"


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


# Open the input CSV file and read Twitter profile URLs

# Open the input CSV file and read Twitter profile URLs
with open(input_file_path, 'r', encoding='utf-8') as infile, open('twitter_profiles_data.csv', 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.DictWriter(outfile, fieldnames=['URL', 'Bio', 'Following Count', 'Followers Count', 'Location', 'Website'])
    writer.writeheader()

    # Iterate over each URL in the input CSV
    for row in reader:
        twitter_url = row[0]
        driver.get(twitter_url)
        time.sleep(5)  # Wait for the page to load

        # Initialize empty variables for profile data
        bio, following_count, followers_count, location, website = "", "", "", "", ""

        try:
            # Use explicit waits and catch exceptions individually for each element
            bio = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='UserDescription']"))
            ).text

            following_count = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-testid='Following']//span"))
            ).text

            followers_count = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-testid='FollowerCount']//span"))
            ).text

            # Check if location and website elements exist, set to empty string if not found
            location_elements = driver.find_elements(By.XPATH, "//span[@data-testid='Location']")
            location = location_elements[0].text if location_elements else ""

            website_elements = driver.find_elements(By.XPATH, "//span[@data-testid='Url']")
            website = website_elements[0].text if website_elements else ""

        except Exception as e:
            print(f"Error scraping data for {twitter_url}: {e}")

        # Write data to the output CSV
        writer.writerow({
            'URL': twitter_url,
            'Bio': bio,
            'Following Count': following_count,
            'Followers Count': followers_count,
            'Location': location,
            'Website': website,
        })

# Close the browser
driver.quit()
