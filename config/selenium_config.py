from selenium import webdriver


options = webdriver.ChromeOptions()

# Adding argument to disable the AutomationControlled flag
options.add_argument("--disable-blink-features=AutomationControlled")

# Exclude the collection of enable-automation switches
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Turn-off userAutomationExtension
options.add_experimental_option("useAutomationExtension", False)

driver_sel = webdriver.Chrome(options=options)
