import requests
import json

def register():
        headers = {"Content-Type": "application/json"}
        register = requests.get('https://145.24.222.82:8443/api/register',
                cert = ('../../certs/T1/t1-server-chain.pem', '../../certs/T1/t1-server-key.pem'),
                verify='../../certs/CAs/noob-root.pem',
                headers=headers)
        print('Register status: ' + str(register.status_code) + ', response: ' + register.text)

def balance():
        headers = {"Content-Type": "application/json"}
        balancePayload = {
                "head":{
                        "fromCtry":"VA",
                        "fromBank":"Berenbank",
                        "toCtry":"VA",
                        "toBank":"Pope banking"
                },
                "body":{
                        "acctNo":"1234567",
                        "pin":"0101"
                }
        }
        bal_data = json.dumps(balancePayload)
        print('Balance request: ' + bal_data)
        b = requests.post('https://145.24.222.236:8443/balance',
                verify=False,
                headers=headers,
                data=bal_data)
        print('Balance status: ' + str(b.status_code) + ', response: ' + b.text)

def withdraw():
        headers = {"Content-Type": "application/json"}
        withdrawPayload = {
                "head":{
                        "fromCtry":"VA",
                        "fromBank":"Berenbank",
                        "toCtry":"VA",
                        "toBank":"Pope banking"
                },
                "body":{
                        "acctNo":"1234567",
                        "pin":"0101",
                        "amount": 5000
                }
        }
        wdw_data = json.dumps(withdrawPayload)
        print('Withdraw request: ' + wdw_data)
        w = requests.post('https://145.24.222.236:8443/withdraw',
                verify=False,
                headers=headers,
                data=wdw_data)
        print('Withdraw status: ' + str(w.status_code) + ', response: ' + w.text)
