import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

invisible = False   # use headless option / "Phantom mode"
url = 'https://opd.financnasprava.sk/#!/check'
# code = 'O-032AF44692974B2EAAF4469297AB2E5F'


def check_receipt(code=None):
    if not code:
        if not len(sys.argv) > 1:
            return
        code = sys.argv[1]

    # SET BROWSER
    cap = DesiredCapabilities.FIREFOX
    cap['marionette'] = True
    options = Options()
    options.headless = invisible
    browser = webdriver.Firefox(capabilities=cap, options=options)
    browser.set_window_size(800, 800)

    # open browser on selected url
    browser.get(url)

    # find input box
    inp = browser.find_element_by_id('input-receipt-id').send_keys(code)

    # find submit button
    browser.find_element_by_id('search-button').click()

    # check availability od "total price" field
    whole = None
    try:
        whole = browser.find_element_by_id('whole-receipt-id-input')
    except NoSuchElementException:
        # invalid document, cannot show whole
        return False
    whole.click()

    browser.find_elements_by_xpath('//table[@class="table-receipt-items"]').click()
    table = browser.find_element_by_xpath('//table[@class="fixed-table table-receipt-items word-wrap"]')

    # iterate through receipt items
    for item in table.find_elements_by_tag_name('tbody'):
        pass

    browser.quit()


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Missing receipt')
        sys.exit()
    code = sys.argv[1]
    result = check_receipt(code)
    if result:
        print('Valid receipt')
    else:
        print('Invalid receipt')
