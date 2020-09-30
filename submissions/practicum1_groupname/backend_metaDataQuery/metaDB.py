from flask import Flask, request
from .metaDataQuery import multiQuery

app = Flask(__name__)


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


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)
