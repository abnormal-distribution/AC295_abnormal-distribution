from flask import Flask, request
from PIL import Image
from io import BytesIO

import base64

from helper.similarity import cosine_dist


app = Flask(__name__)


@app.route("/",methods=['POST','GET'])
def mainm():
    if request.method == 'POST':
        image = request.get_json()['image']  # Retrieve the image submitted by the user
        image = image.encode('ascii')
        image = base64.b64decode(image)
        image = Image.open(BytesIO(image))
        
        img_id = cosine_dist(image)
        
        return img_id

    else:
        return 'This is GET method'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8083, debug=True)
