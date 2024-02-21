import json

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from fake_useragent import UserAgent
from config.logger import setup_logger


logger = setup_logger(__name__)


def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


def add_script(driver, script):
    send(driver, "Page.addScriptToEvaluateOnNewDocument", {"source": script})


WebDriver.add_script = add_script

options = webdriver.ChromeOptions()

my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
# my_user_agent = UserAgent()

# options.add_argument('--no-sandbox')
# options.add_argument('--headless=new')

options.add_argument(f"--user-agent={my_user_agent}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver_sel = webdriver.Chrome(options=options)

# driver_sel = webdriver.Remote(
#     command_executor='http://172.18.0.2:4444/wd/hub',
#     options=options
# )

driver_sel.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

add_script(driver_sel,
           '''
                  delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                  delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                  delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
                  delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                  delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            '''
           )

logger.debug(driver_sel.execute_script("return navigator.userAgent"))
