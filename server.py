from flask import Flask, request, send_from_directory
from figo import FigoConnection, FigoSession
import os
import webbrowser


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/account')
def account():
  session = FigoSession("ASHWLIkouP2O6_bgA2wWReRhletgWKHYjLqDaqb0LFfamim9RjexTo22ujRIP_cjLiRiSyQXyt2kM1eXU2XLFZQ0Hro15HikJQT_eNeT_9XQ")
  print session
  securities = session.securities
  #for security in session.get_securities():
  #  print security
  return 'alkjalkaj';


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('/static', path)

@app.route('/')
def index():
	return app.send_static_file('index.html')

if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port, debug=True)
