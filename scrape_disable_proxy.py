from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Set Firefox options
options = Options()
options.headless = False  # Set to True to run in background

# Disable the proxy
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = ''
proxy.ssl_proxy = ''
options.proxy = proxy

# Initialize the Firefox driver with the options
driver = webdriver.Firefox(options=options)

# Open a website
driver.get("https://www.weather.com")
driver.get("https://www.uc.edu")

# Print the title of the page
print(driver.title)

# Close the browser window
driver.quit()
