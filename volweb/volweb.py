from bottle import route, run

@route('/hello')
def hello():
    return "Volumes Web App!"

run(host='localhost', port=8080, debug=True)
