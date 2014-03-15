from bottle import route, run, response, request
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

@route('/img', method='GET')
def img():
    # read query values
    vals = {'w':100, 'h':100, 'r':255, 'g':0, 'b':0}
    for key in vals.keys():
        tmp = request.query.get(key)
        if tmp:
            vals[key] = int(tmp)
    # set response
    response.content_type = 'image/png'
    # create image
    im = Image.new('RGB', (vals['w'], vals['h']), 
                   (vals['r'], vals['g'], vals['b']))
    # send as bytes
    strData = io.BytesIO()
    im.save(strData, 'PNG')
    strData.seek(0)
    return strData.getvalue()

@route('/rimg')
def rimg():
    im = createRandomTile((100, 100))
    response.content_type = 'image/png'
    strData = io.BytesIO()
    im.save(strData, 'PNG')
    strData.seek(0)
    return strData.getvalue()

run(host='192.168.4.3', port=8080, debug=True)
