from microHTTP import HttpServer, Response, req


app = HttpServer()


@app.add_route('/', methods=['GET'])
def main(request):
    print(request.method)
    return Response(status=200, template='index.html')


app.run(host='0.0.0.0', port=7000)
