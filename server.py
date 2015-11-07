from flask import Flask, request, send_from_directory
import os

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('/static', path)

@app.route('/')
def index():
	return app.send_static_file('index.html')

if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port, debug=True)