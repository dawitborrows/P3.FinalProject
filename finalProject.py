import urllib.parse, urllib.request, urllib.error, json
import requests

from io import BytesIO
from PIL import Image
from PIL import ImageChops
from PIL import ImageFilter
from flask import Flask, render_template, request
from flask import Flask, url_for
#from PIL import cv2
import os
app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

     #parse dictionary
     #populate my_dict
# gets a random photo in this category/query
# query: any search term for photos
#######add n
def get_photo_data(query):
    dictionary = {"client_id": "dbN8l-IceuKN-OXJzRATU4z8cSEli8EcT3GA0ZreTjo", "query": query, "count": 20}
    urlDict = urllib.parse.urlencode(dictionary)
    baseurl = "http://api.unsplash.com/photos/random"
    url = baseurl + "?" + urlDict
    r = urllib.request.urlopen(url)
    photorequest = r.read()
    photodata = json.loads(photorequest)
    return photodata



# colors = input ("What colors do you want to work with? ")
# comma entry or selection using HTML
# size = input ("What ")
colorList = ["red", "purple", "green", "blue"]# , "pink", "orange", "white", "grey"] #whatever colors are given

#save a image using extension
#im1 = im1.save("geeks.jpg", "jpg")
#picture = picture.save("dolls.jpg")
def editFiles(url, width, height, colorList = ["red", "green", "blue"]): #colorList = ["red", "green", "blue"]):   
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
    #img.filter(ImageFilter.BLUR).save("/Users/dawitborrows/Documents/GitHub/FinalProject/Static/%s"%str(n) + ".jpg")
    #img.resize((width * n, height * n)).save("/Users/dawitborrows/Documents/GitHub/FinalProject/Static/resize" + ".jpg")
    

#when getting a module not found error, in terminal, type "pip3 install <module>"
  
linkDict = {} #dictionary for links
def utility_func(dictionary = {}, linkDict = {}): # dictionary for photo objects
    n = 0   
    for key in dictionary:
        linkDict["photo%s"%str(n)]= dictionary[n]["urls"]["full"] 
        n += 1

@app.route('/')
def homepage():
    app.logger.info("In MainHandler")
    return render_template('homepage.html')

# create a list of photo objects
@app.route('/photo')
def search_handler():
    term = request.args.get('searchterm')
    if term:
        #######add n
        dictionary = get_photo_data(term)
        list =[]
        n = 0
        for photo in dictionary:
            list.append(photo["urls"]["full"])
        return render_template('unsplash.html', page_title="Results for search", list = list)#, photo = photo)




#create a form of images that links to somewhere
#input colors
#separate files for blending, addig, etc.?
#css decorations
@app.route('/photo/edit')
def view_edits():
    url = request.args.get("Image")
    #link = linkDict[address]
    img_data = requests.get(url).content    
    im = Image.open(BytesIO(img_data))
    im.size
    width = im.size[0]
    height = im.size[1]
    colorList = []
    response = request.args.get("color")
    colors = response.split(',')
    for color in colors:
        colorList.append(color)
    #resolutionEnhancement = request.args.get("resolution")
    editFiles(url, width, height, colorList)
    edittedList = []
    n = 0
    # +1 for hte black and white
    path = "/Users/dawitborrows/Documents/GitHub/FinalProject/Static/"
    for i in range(len(colorList) + 1):
        edittedList.append(str(n))
        n += 1

    return render_template('Thematic.html', edittedList = edittedList)

    
if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)


