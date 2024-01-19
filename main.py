import socket
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))


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


def configure_port_forwarding(data, local_ip):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(f"{os.getcwd()}/chromedriver.exe"))

    try:
        # Open the router's web interface on the virtual server page
        driver.get(
            f"http://{data['username']}:{data['password']}@{data['router_ip']}/scvrtsrv.cmd?action=view"
        )

        # Wait for the page to load
        time.sleep(3)

        # Get the checkbox to remove the previous port forward (there will always be one)
        checkbox = driver.find_element(By.NAME, "rml")

        current_forwarded_ip = checkbox.get_attribute("value").split("|")[0]

        if current_forwarded_ip == local_ip:
            print("Server already forwarded")
            driver.quit()
            return

        print("Server not forwarded, press enter to proceed with forwarding")
        input()

        checkbox.click()
        time.sleep(10)

    finally:
        # Close the browser window
        driver.quit()


if __name__ == "__main__":
    # load the data
    with open(f"{os.getcwd()}/data.json", "r") as f:
        data = json.load(f)

    # Get and print the local IP address
    local_ip = get_local_ip()

    if local_ip:
        print(f"Local IP Address: {local_ip}")
    else:
        print("Failed to retrieve local IP address.")
        quit()

    configure_port_forwarding(data, local_ip)
