from selenium import webdriver
from selenium.webdriver.common.by import By  # for finding dimensions of screenshot
from reddit_grab import post1  # importing reddit post object
import time  # so webpage can load before screenshotting
from PIL import Image
import io

driver = webdriver.Safari()
driver.get(post1.url)

# for verification
print(post1.url)

time.sleep(5)

element = driver.find_element(By.CSS_SELECTOR, 'shreddit-post')
location = element.location
size = element.size

screenshot = driver.get_screenshot_as_png()

# Use Pillow to open the screenshot
image = Image.open(io.BytesIO(screenshot))

# Calculate the coordinates of the crop box
left = location['x']
top = location['y']
right = left + size['width']
bottom = top + size['height']

# Crop the screenshot to the element's dimensions
cropped_image = image.crop((left, top, right, bottom))

# Save the cropped screenshot
cropped_image.save('element_screenshot.png')

# Close the WebDriver
driver.quit()

driver.quit()
