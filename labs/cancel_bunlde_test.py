import requests
from selenium import webdriver
from selenium.webdriver.common.by import By



# Make a POST request
url = "https://examerp.keralauniversity.ac.in/cd-unit/bundle-cancel"
payload = {
    "bundle_id": "28918"
}
headers= {
        "X-CSRFToken": "y2yLl6bR4oPqPmzBmyxTpIvXgK3N9a7sESYWdMR0KMHZPjJrjYUqorqob6RZ6dq1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
response = requests.post(url, json=payload, headers=headers, verify=False)

# Print the response
print(response.json())