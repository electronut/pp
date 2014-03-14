from bottle import route, run, response
from PIL import Image, ImageDraw
import random
import io
from autos import createRandomTile

@route('/hello')
def hello():
    return "Hello Bottle!"

@route("/test_template")
def test_template(): 
    return '<h4>Random Tile </h4><img src="/img" />';

@route('/img')
def img():
    im = createRandomTile((100, 100))
    response.content_type = 'image/png'
    strData = io.BytesIO()
    im.save(strData, 'PNG')
    strData.seek(0)
    return strData.getvalue()

run(host='192.168.4.3', port=8080, debug=True)
