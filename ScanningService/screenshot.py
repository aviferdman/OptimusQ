from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep

# driver = webdriver.Firefox()
# driver = webdriver.Chrome()
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
#
# driver.get('https://www.bbc.com/storyworks/clear-sky-thinking-airbus-2021/airbus-2021-clear-sky-thinking-?utm_source=taboola&utm_medium=native&tblci=GiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ#tblciGiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ')
# sleep(1)
#
# driver.get_screenshot_as_file("screenshot.png")
# driver.quit()

url = 'https://stackoverflow.com/'
path = 'scrapedScreen.png'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
# el = driver.find_element_by_tag_name('body')
el = driver.find_element(By.CLASS_NAME, "body")

el.screenshot(path)
driver.quit()
print("end...")