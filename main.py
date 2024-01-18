import socket


def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to an external server (doesn't actually send data)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address
        local_ip = s.getsockname()[0]

        return local_ip
    except socket.error as e:
        print(f"Error: {e}")
        return None
    finally:
        # Close the socket
        s.close()


# Get and print the local IP address
local_ip = get_local_ip()

if local_ip:
    print(f"Local IP Address: {local_ip}")
else:
    print("Failed to retrieve local IP address.")


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def configure_port_forwarding(
    router_ip, username, password, internal_ip, internal_port, external_port
):
    # Set up the Selenium WebDriver (make sure to replace the path with the path to your webdriver executable)
    driver = webdriver.Chrome(executable_path="/path/to/chromedriver")

    try:
        # Open the router's web interface
        driver.get(f"http://{router_ip}")

        # Find and fill in the username and password fields
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)

        # Submit the login form
        driver.find_element_by_id("loginBtn").click()

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(2)

        # Navigate to the port forwarding section (replace with the actual link or button ID)
        driver.get("http://{router_ip}/port_forwarding")

        # Fill in the port forwarding details
        driver.find_element_by_name("internal_ip").send_keys(internal_ip)
        driver.find_element_by_name("internal_port").send_keys(internal_port)
        driver.find_element_by_name("external_port").send_keys(external_port)

        # Submit the port forwarding form (replace with the actual button or form submission method)
        driver.find_element_by_id("submitBtn").click()

    finally:
        # Close the browser window
        driver.quit()


# Replace the placeholders with your router's information
router_ip = "your_router_ip"
username = "your_router_username"
password = "your_router_password"
internal_ip = "internal_device_ip"
internal_port = "internal_device_port"
external_port = "external_port"

configure_port_forwarding(
    router_ip, username, password, internal_ip, internal_port, external_port
)
