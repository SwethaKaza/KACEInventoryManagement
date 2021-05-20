import requests
import urllib3
import json
import time
from getpass import getpass

# Prevents the SSL certificate warning from appearing in the output
urllib3.disable_warnings()

# URL for KACE API login
authRequest = "https://yourkacedomain.com/ams/shared/api/security/login"

# Get KACE user credentials
userID = input("KACE API username: ")
userPass = getpass(prompt="KACE API password: ", stream=None)

# Construct payload to be sent in the body of the request
payload = {
    "password":userPass,
    "userName":userID,
    "organizationName":"Default"
}

payload = json.dumps(payload)

# Construct request headers
authHeaders = {
  "Accept": "application/json",
  "Content-Type": "application/json",
  "x-dell-api-version": "1"
}

# Make the POST request to login
authResponse = requests.request("POST", authRequest, headers=authHeaders, data=payload, verify=False)

# Extract CSRF token to be used as header in GET requests going forward
csrfToken = authResponse.headers['x-dell-csrf-token']

# Process authentication response
print(json.dumps(authResponse.json(), indent=4, sort_keys=True))

# URL for dumping machine inventory from KACE
deviceInventory = "https://yourkacedomain.com/api/inventory/machines"

# Construct request headers
inventoryHeaders = {
  "x-dell-csrf-token":csrfToken,
  "Accept": "application/json",
  "Content-Type": "application/json",
  "x-dell-api-version": "1"
}

# Make the GET request to dump machine inventory
inventoryResponse = requests.request("GET", deviceInventory, headers=inventoryHeaders, cookies=authResponse.cookies, verify=False)

# Process inventory dumps
inventoryDump = json.dumps(inventoryResponse.json(), indent=4, sort_keys=True)

currentTime = time.strftime("%Y%m%d-%H%M%S")
with open("InventoryDump_" + currentTime + ".json", "w") as outfile:
    outfile.write(inventoryDump)
