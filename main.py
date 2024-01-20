import socket
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

        remove_checkbox = None

        try:
            # Get the checkbox to remove the previous port forward (there will always be one)
            remove_checkbox = driver.find_element(By.NAME, "rml")

            current_forwarded_ip = remove_checkbox.get_attribute("value").split("|")[0]

            if current_forwarded_ip == local_ip:
                print("Server already forwarded")
                driver.quit()
                return

        except:
            pass

        print("Server not forwarded, forwarding now")

        # From here on we need to remove it by clicking it followed by the remove button (if it exists)
        if remove_checkbox:
            remove_checkbox.click()

            # Click remove button
            driver.find_element(By.ID, "sevrtview_remove").click()

        # Wait for page to reload
        time.sleep(1)

        # Click the add button
        driver.find_element(By.ID, "sevrtview_add").click()

        # Wait for page to reload
        time.sleep(1)

        # Find and select the interface in the selection dropdown
        Select(driver.find_element(By.NAME, "dstWanIf")).select_by_value("ppp2.1")

        # Click to name it as a custom service, we need to click the 2nd one for a custom service
        driver.find_elements(By.NAME, "radiosrv")[1].click()

        # Name the service. In this case just name it minecraft server
        driver.find_element(By.NAME, "cusSrvName").send_keys("Minecraft server")

        # Set the server IP to the local IP (the last digits as they designate the device) i.e 192.168.20.xx
        driver.find_element(By.NAME, "sIp").send_keys(local_ip.split(".")[-1])

        # Enable it in the status dropdown
        Select(driver.find_element(By.NAME, "status")).select_by_value("1")

        # Set the port start and end numbers
        driver.find_element(By.NAME, "eStart").send_keys("25565")
        driver.find_element(By.NAME, "eEnd").send_keys("25565")

        # Select the TCP/UDP option
        Select(driver.find_element(By.NAME, "proto")).select_by_value("0")

        # Finally click apply and save
        driver.find_element(By.ID, "natSaveApply").click()

        print("Server forwarded successfully")
        time.sleep(5)

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
