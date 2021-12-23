from selenium import webdriver
from PIL import Image
from io import BytesIO
# from cStringIO import StringIO
from webdriver_manager.chrome import ChromeDriverManager
def take_web_screenshot(url):
    verbose = 1

    browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser.get(
    #     'https://www.bbcgoodfood.com/howto/guide/top-10-winter-drinks')
    browser.get(url)

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

    screenshot.save('screenshots/' + 'page_screenshot' + '.png')
