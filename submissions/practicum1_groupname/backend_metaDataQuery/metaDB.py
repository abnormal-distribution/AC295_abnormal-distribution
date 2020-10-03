from flask import Flask, request

from helper.metaDataQuery import multiQuery


PATH = "/meta-data/metadata.csv"
"""
PATH = 'gs://practicum1-abnormal-distribution/data/metadata.csv'
"""


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def mainm():
    if request.method == 'POST':
        image_name = request.get_json()['image_name']  # Retrieve the image name submitted by the user

        metadata = multiQuery(image_name, PATH)  # Load database with Dask
        metadata = metadata[['file_id', 'Title']].to_dict(("list"))
        
        return metadata

    else:
        return 'This is GET method'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)
