from selenium import webdriver
from PIL import Image
from io import BytesIO
# from cStringIO import StringIO
from webdriver_manager.chrome import ChromeDriverManager

# Component responsible for saving a screenshot of the landing page

verbose = 1

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(
    'https://www.bbc.com/storyworks/clear-sky-thinking-airbus-2021/airbus-2021-clear-sky-thinking-?utm_source=taboola&utm_medium=native&tblci=GiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ#tblciGiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ')

# from here http://stackoverflow.com/questions/1145850/how-to-get-height-of-entire-document-with-javascript
js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

scrollheight = browser.execute_script(js)

if verbose > 0:
    print(scrollheight)

slices = []
offset = 0
while offset < scrollheight:
    if verbose > 0:
        print(offset)

    browser.execute_script("window.scrollTo(0, %s);" % offset)
    img = Image.open(BytesIO(browser.get_screenshot_as_png()))
    offset += img.size[1]
    slices.append(img)

    if verbose > 0:
        browser.get_screenshot_as_file('%s/screen_%s.png' % ('/tmp', offset))
        print(scrollheight)

screenshot = Image.new('RGB', (slices[0].size[0], scrollheight))
offset = 0
for img in slices:
    screenshot.paste(img, (0, offset))
    offset += img.size[1]

screenshot.save('test.png')
