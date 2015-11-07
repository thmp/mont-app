# -*- coding=utf8 -*-

from flask import Flask, request, send_from_directory
from figo import FigoConnection, FigoSession
import os
import webbrowser, json
import requests

KEYDICT = {'KeyId': '782f60c6-f1a3-4670-84fe-5b3c749ceddc'}

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

my_securities = [
  {
    'name': 'iShares Core MSCI World',
    'amount': u'€ 3,144.01'
  }
]

@app.route('/account')
def account():
  r = requests.get('https://ucg-apimanager.axwaycloud.net:8065/accounts/v1?userId=aa.bruno.60', headers=KEYDICT)
  account_ids = []
  accounts = r.json()['accounts']
  account_info = []
  for account in accounts:
    account_ids.append(account['account']['id'])
    r = requests.get('https://ucg-apimanager.axwaycloud.net:8065/accounts/v1/'+account['account']['id']+'?userId=aa.bruno.60', headers=KEYDICT)
    account_info.append({'name': r.json()['account']['name'], 'balance': r.json()['account']['balance']})
  return json.dumps(account_info)

@app.route('/securities')
def securities():
  return json.dumps(my_securities)

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('/static', path)

@app.route('/')
def index():
	return app.send_static_file('index.html')

if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port, debug=True)
