from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/trigger', methods=['POST'])
def trigger():
    if request.method == 'POST':
        print request.json
        return str(request.json)
    else:
        return 'Not supported'

if __name__ == '__main__':
    app.run()
