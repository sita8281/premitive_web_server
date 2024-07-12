from microHTTP import HttpServer


app = HttpServer()


@app.add_route('/', methods=['GET'])
def main():
    return 'test'


app.run(host='0.0.0.0', port=7000)
