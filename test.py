from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello!', 200


app.run(host='0.0.0.0', port=8000)