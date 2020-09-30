from flask import Flask, render_template, request
import sys
import requests
import numpy as np
from base64 import b64encode

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def mainm():
    return render_template('index.html') # first page 

@app.route('/search', methods=['POST', 'GET'])
def simpleSearch():
    if request.method == 'POST':  # User clicked submit button
        image_name = request.form['content'] # Get image name submitted by user
        image_file = requests.post(url=db_url, json={'image_name': image_name}) # request image file from database
        #full_filename = 'http://0.0.0.0:32500' + image_file.content.decode("utf-8")
        return render_template('searchResult.html',
                               title=image_name,
                               image_url=image_file.content.decode("utf-8")) # render html with image
    else:
        print("This is the get method.")

@app.route('/upload', methods=['POST', 'GET'])
def uploadImage():
    if request.method == 'POST':
        encoded = b64encode(request.files['file'].read())
        imgbase64 = encoded.decode('ascii')
        mime = "image/jpeg"
        uri = "data:%s;base64,%s" % (mime, imgbase64)
        return render_template("searchResult.html", image_url=uri, title="Uploaded Image")
    else:
        print("This is the get method.")


if __name__ == "__main__":
    # determine what the URL for the database should be, port is always 8082 for DB

    if (len(sys.argv) >= 2):
        db_url = 'http://' + sys.argv[1] + ':8082'
    else:
        db_url = "http://0.0.0.0:8082/"

    app.run(host='0.0.0.0', port=8081, debug=True)
