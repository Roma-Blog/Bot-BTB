import requests

url = 'https://api.direct.yandex.ru/live/v4/json/'


def getBalance(nameAccount, data_json):
   body = {
         'method': 'AccountManagement',
         'param': {
            'Action': 'Get',
            'SelectionCriteria': {}
         },
         'locale': 'ru',
         'token': data_json[nameAccount]['token']
      }
   
   if (data_json[nameAccount]['agent_account'] == True):
      body['param']['SelectionCriteria']['Logins'] = [data_json[nameAccount]['login']]

   r = requests.post(url, 
      json= body,
      headers={
         'Content-Type': 'application/json'
      })
   
   ## print("Статус ", r.status_code)
   if(r.status_code>=200):
      ## print(r.json())
      return r.json()['data']['Accounts'][0]['Amount']
   else:
      file_error = open("ErrorAPI.txt", "w+")
      file_error.write(f"{r.status_code}, {r.json()}")
      file_error.close()
   
   