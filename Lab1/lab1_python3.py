#Run this with python 3.

import requests

print("version of requests: ", requests.__version__,'\n') #Printing out version of Requests

response = requests.get("http://google.com")
print(response.status_code)

response = requests.get("http://ccid-eddieantonio.rhcloud.com/touqir")
print(response.status_code)