import json, directapi


def readData ():
    with open('data.json', 'r') as elem:
        return json.load(elem)

def getListAccounts (data_json):
    list_accounts = {}
    for key in data_json:
        if (key != "admin"):
            list_accounts[key] = data_json[key]["account_id"]
    return list_accounts

def setBalansInData(list_accounts, data_json):
    for key in list_accounts:
        balance = directapi.getBalance(key, data_json)
        data_json[key]['balance'] = int(float(balance))
    return data_json



