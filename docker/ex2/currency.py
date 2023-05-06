import requests

# retrieves some data using a request
url = "https://open.er-api.com/v6/latest/CAD"
req = requests.get(url)
data = req.json()

# prints the current exchange rate between USD and CAD
print('Today for 1 CAD you can buy ', data['rates']['USD'], ' USD')
