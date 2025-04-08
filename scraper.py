from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Configure Firefox proxy settings for mitmproxy
firefox_options = Options()
firefox_options.set_preference("network.proxy.type", 1)
firefox_options.set_preference("network.proxy.http", "localhost")
firefox_options.set_preference("network.proxy.http_port", 8080)
firefox_options.set_preference("network.proxy.ssl", "localhost")
firefox_options.set_preference("network.proxy.ssl_port", 8080)
firefox_options.set_preference("network.proxy.allow_hijacking_localhost", True)
firefox_options.set_preference("security.enterprise_roots.enabled", True)

# Set the path to Geckodriver
service = Service("/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=service, options=firefox_options)

# URLs to visit
urls = [
    "https://www.cnn.com",
    "https://testphp.vulnweb.com",
    "https://zero.webappsecurity.com"
]

for url in urls:
    driver.get(url)
    print(f"Visited: {url}")

driver.quit()
print("✅ Finished browsing!")
