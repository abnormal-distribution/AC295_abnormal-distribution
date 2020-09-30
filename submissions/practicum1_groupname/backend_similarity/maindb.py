from flask import Flask, request
import dask.dataframe as dd

app = Flask(__name__)


@app.route("/",methods=['POST','GET'])
def mainm():
    if request.method=='POST':
        image_name = request.get_json()['image_name'] # Retrieve the image name submitted by the user

        metadata = dd.read_csv('data/metadata.csv') # Load database with Dask
        try:
            file_id = metadata.file_id[metadata.Title == image_name].compute().values[0] # Get file_id for image

            return '/static/gap_images/{}'.format(file_id) # return static address

        except IndexError:
            return 'Painting not in the database'

    else:

        return 'This is GET method'


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)