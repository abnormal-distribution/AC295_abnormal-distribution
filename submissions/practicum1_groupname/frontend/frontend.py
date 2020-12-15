from flask import Flask, render_template, request
import sys
import requests
import numpy as np
from base64 import b64encode
from gcsfs import GCSFileSystem

app = Flask(__name__)

#gcs = GCSFileSystem(project='ac295-data-science-289004')
#gcs.ls('practicum1-abnormal-distribution')

google_metadata_dir = 'gs://practicum1-abnormal-distribution/data/metadata.csv'
google_bucket_dir = 'https://storage.googleapis.com/practicum1-abnormal-distribution/static/gap_images/'


@app.route("/", methods=['POST', 'GET'])
def mainm():
    return render_template('index.html') # first page 

@app.route('/search', methods=['POST', 'GET'])
def simpleSearch():
    if request.method == 'POST':  # User clicked submit button
        image_name = request.form['content'] # Get image name submitted by user
        image_file = requests.post(url=db_url_2, json={'image_name': image_name}) # request image files from database
        image_file = image_file.json()
        file_id = [google_bucket_dir + image for image in image_file['file_id'][:5]]
        title = image_file['Title'][:5]
        numberings = np.arange(len(file_id))
        return render_template('searchResult.html', numberings = numberings, images=zip(numberings,file_id,title))

    else:
        print("This is the get method.")

@app.route('/upload', methods=['POST', 'GET'])
def uploadImage():
    if request.method == 'POST':
        # encoding the uploaded image to base64
        encoded = b64encode(request.files['file'].read())
        imgbase64 = encoded.decode('ascii')
        mime = "image/jpeg"
        uri = "data:%s;base64,%s" % (mime, imgbase64)

        # request image file from database
        image_file = requests.post(url=db_url_1, json={'image': imgbase64})
        final_address = google_bucket_dir + "gap_" + image_file.content.decode("utf-8")+".jpg"
        return render_template("similarityResult.html", similar_image_url = final_address,
            image_url=uri, title="Uploaded Image")
    else:
        print("This is the get method.")


if __name__ == "__main__":
    # determine what the URL for the database should be, port is always 8082 for DB

    if (len(sys.argv) >= 2):
        db_url_1 = 'http://' + sys.argv[1] + ':8082'
        db_url_2 = 'http://' + sys.argv[2] + ':8083'
    else:
        db_url_1 = "http://0.0.0.0:8082/"
        db_url_2 = "http://0.0.0.0:8083/"

    app.run(host='0.0.0.0', port=8081, debug=True)
