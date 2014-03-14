from bottle import route, run, response
from PIL import Image, ImageDraw
import random
import io

@route('/hello')
def hello():
    return "Hello Bottle!"

# create image filled with random dots
def createRandomTile(dims):
  # create image
  img = Image.new('RGB', dims)
  draw = ImageDraw.Draw(img)
  # calculate radius - % of min dimension 
  r = int(min(*dims)/100)
  # number of dots
  n = 1000
  # draw random circles
  for i in range(n):
    # -r is used so circle stays inside - cleaner for tiling
    x, y = random.randint(0, dims[0]-r), random.randint(0, dims[1]-r)
    fill = (random.randint(0, 255), random.randint(0, 255), 
            random.randint(0, 255))
    draw.ellipse((x-r, y-r, x+r, y+r), fill)
  # return image
  return img

@route("/test_template")
def test_template(): 
    return '<h4>Random Tile Image</h4><img src="/img" />';

@route('/img')
def img():
    im = createRandomTile((100, 100))
    response.content_type = 'image/png'
    strData = io.BytesIO()
    im.save(strData, 'PNG')
    strData.seek(0)
    return strData.getvalue()

run(host='192.168.4.3', port=8080, debug=True)
