import requests
import json
import testfunctions as testfunc

test = requests.post("https://145.24.222.236:8443/balance", cert=("/home/ubuntu-1064501/certs/test_certificate.crt", "/home/ubuntu-1064501/certs/test_key.pem"), verify=False)
# print(test.text)

# testfunc.balance()
testfunc.withdraw()