from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Set up Firefox options
firefox_options = Options()
firefox_options.set_preference("network.proxy.type", 1)  # Manual proxy configuration
firefox_options.set_preference("network.proxy.http", "localhost")
firefox_options.set_preference("network.proxy.http_port", 8080)
firefox_options.set_preference("network.proxy.ssl", "localhost")
firefox_options.set_preference("network.proxy.ssl_port", 8080)
firefox_options.set_preference("network.proxy.allow_hijacking_localhost", True)
firefox_options.set_preference("security.enterprise_roots.enabled", True)  # Use system certificates

# Path to Geckodriver (update if needed)
service = Service("/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=service, options=firefox_options)

# URLs to visit
urls = [
    "http://example.com",
    "http://testphp.vulnweb.com",
    "http://zero.webappsecurity.com"
]

for url in urls:
    driver.get(url)  # Open URL
    print(f"Visited: {url}")

driver.quit()  # Close browser
