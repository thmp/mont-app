# -*- coding=utf8 -*-

from flask import Flask, request, send_from_directory, make_response
from figo import FigoConnection, FigoSession
from functools import wraps
import os
import webbrowser, json
import requests
from watson_developer_cloud import ConceptInsightsV2 as ConceptInsights
from requests.auth import HTTPBasicAuth

def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

KEYDICT = {'KeyId': '782f60c6-f1a3-4670-84fe-5b3c749ceddc'}
ALCHEMY = '5a8e248d968514b30bad5d7fc814937cc9663257'

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

@app.route('/transactions')
def transactions():
  r = requests.get('https://ucg-apimanager.axwaycloud.net:8065/transactions/v1?userId=aa.bruno.60', headers=KEYDICT)
  transactions = r.json()['transactions']
  transaction_info = []
  for transaction in transactions:
    transaction_info.append({'description': transaction['description'], 'amount': transaction['amount']})
  return json.dumps(transaction_info[:10])

@app.route('/more/<query>')
def more(query):
  ##r = requests.get('http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords?outputMode=json&apikey='+ALCHEMY+'&text='+query)

  #keywords = []
  #for word in r.json()['keywords']:
  #  keywords.append(word['text'])

  r = requests.post('https://concept-insights-demo.mybluemix.net/api/extractConceptMentions', data={'text': query})
  annotations = []
  print r.text
  for annotation in r.json()['annotations']:

    r1 = requests.get('https://gateway.watsonplatform.net/concept-insights/api/v2/graphs/wikipedia/en-20120601/related_concepts?concepts=["/graphs/wikipedia/en-20120601/concepts/'+annotation['concept']['label']+'"]&level=1', auth=HTTPBasicAuth('c4f1a04e-1a41-4b96-b60b-a79f525200ad', 'DNnG37PURhHk'))
    related = []
    for concept in r1.json()['concepts']:
      related.append({'title': concept['concept']['label']})

    annotations.append({'title': annotation['concept']['label'], 'related': related})

  return json.dumps(annotations)

@app.route('/stock/<query>')
@add_response_headers({'Access-Control-Allow-Origin': '*'})
def search(query):
  r = requests.get('http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities?outputMode=json&apikey='+ALCHEMY+'&text='+query)

  if len(r.json()['entities']) >= 0:
    query = ''
    for entity in r.json()['entities']:
      if entity['type'] == 'Company':
        query = entity['text']
    r = requests.get('https://s.yimg.com/aq/autoc?query='+query+'&region=US&lang=en-US&callback=callback')
    resp = r.text[9:-2]
    resp_json = json.loads(resp)

    stocks = []
    for stock in resp_json['ResultSet']['Result']:
      stocks.append(stock['symbol'])

    if len(stocks) == 0:
      return json.dumps([])

    # get quotes for stocks
    symbols = ",".join(stocks)
    r = requests.get('http://finance.yahoo.com/webservice/v1/symbols/'+symbols+'/quote?format=json&view=detail')
    quotes = r.json()['list']['resources']
    quotes_list = []
    for quote in quotes:
      quotes_list.append({
        'name': quote['resource']['fields']['name'],
        'price': quote['resource']['fields']['price'],
        'symbol': quote['resource']['fields']['symbol']
        })
    return json.dumps(quotes_list[:5])
  else:
    return json.dumps([])

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
