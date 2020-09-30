from flask import Flask, request
from helper.metaDataQuery import verySimpleQuery
from gcsfs import GCSFileSystem

app = Flask(__name__)

gcs = GCSFileSystem(project='ac295-data-science-289004')
gcs.ls('practicum1-abnormal-distribution')

google_metadata_dir = 'gs://practicum1-abnormal-distribution/data/metadata.csv'
google_bucket_dir = 'https://storage.googleapis.com/practicum1-abnormal-distribution/static/gap_images/'


@app.route("/", methods=['POST', 'GET'])
def mainm():
    if request.method == 'POST':
        image_name = request.get_json()['image_name']  # Retrieve the image name submitted by the user

        metadata = verySimpleQuery(image_name, google_metadata_dir)  # Load database with Dask
        try:
            file_id = verySimpleQuery(image_name, google_metadata_dir)  # Load database with Dask  # Get file_id for image
            final_address = google_bucket_dir + file_id

            return final_address # return static address

        except IndexError:
            return 'Painting not in the database'

    else:

        return 'This is GET method'


"""
@app.route("/",methods=['POST','GET'])
def mainm():
    if request.method=='POST':
        image_name = request.get_json()['image_name'] # Retrieve the image name submitted by the user

        metadata = multiQuery(image_name)

        if metadata.shape[0] == 0:
            return 'Painting not in the database'
        else:
            return metadata

    else:

        return 'This is GET method'
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)
