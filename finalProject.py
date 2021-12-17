import urllib.parse, urllib.request, urllib.error, json
import requests

from io import BytesIO
from PIL import Image
from PIL import ImageChops
from PIL import ImageFilter
from flask import Flask, render_template, request
from flask import Flask, url_for
import os
app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# uses the Unsplash API to get a random photo in this category/query
# query: any search term for photos
def get_photo_data(query):
    dictionary = {"client_id": "dbN8l-IceuKN-OXJzRATU4z8cSEli8EcT3GA0ZreTjo", "query": query, "count": 20}
    urlDict = urllib.parse.urlencode(dictionary)
    baseurl = "http://api.unsplash.com/photos/random"
    url = baseurl + "?" + urlDict
    r = urllib.request.urlopen(url)
    photorequest = r.read()
    photodata = json.loads(photorequest)
    return photodata


# edits the chosen image
def editFiles(url, width, height, colorList = ["red", "green", "blue"]):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    n = 0
    img.convert("L").save("/Users/dawitborrows/Documents/GitHub/FinalProject/Static/%s"%str(n) + ".jpg")
    n += 1
    for color in colorList:
        screen = Image.new("RGB", (width, height), color)
        img = img.convert("RGB")
        blend = Image.blend(img,screen,0.2)    
        blend.save("/Users/dawitborrows/Documents/GitHub/FinalProject/Static/%s"%str(n) + ".jpg")
        n += 1

# homepage
@app.route('/')
def homepage():
    app.logger.info("In MainHandler")
    return render_template('homepage.html')

# page that shows results for search
@app.route('/photo')
def search_handler():
    term = request.args.get('searchterm')
    if term:
        dictionary = get_photo_data(term)
        list =[]
        n = 0
        for photo in dictionary:
            list.append(photo["urls"]["full"])
        return render_template('unsplash.html', page_title="Results for search", list = list)#, photo = photo)

#final output
@app.route('/photo/edit')
def view_edits():
    url = request.args.get("Image")
    img_data = requests.get(url).content    
    im = Image.open(BytesIO(img_data))
    width = im.size[0]
    height = im.size[1]
    colorList = []
    response = request.args.get("color")
    colors = response.split(',')
    for color in colors:
        colorList.append(color)
    editFiles(url, width, height, colorList)
    edittedList = []
    n = 0
    path = "/Users/dawitborrows/Documents/GitHub/FinalProject/Static/"
    for i in range(len(colorList) + 1):
        edittedList.append(str(n))
        n += 1
    return render_template('Thematic.html', edittedList = edittedList)

    
if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)


