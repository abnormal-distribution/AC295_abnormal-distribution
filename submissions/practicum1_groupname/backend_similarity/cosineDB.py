from flask import Flask, request
from PIL import Image
from io import BytesIO

import base64

from helper.similarity import cosine_dist


USERNAME = "/secrets/username"
PASSWORD = "/secrets/password"


app = Flask(__name__)


@app.route("/",methods=['POST','GET'])
def mainm():
    if request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        image = request.get_json()['image']  # Retrieve the image submitted by the user
        
        with open(USERNAME, 'r') as f:
            user = f.read()

        with open(PASSWORD, 'r') as f:
            keyword = f.read()

        if user == username and keyword == password:
            image = image.encode('ascii')
            image = base64.b64decode(image)
            image = Image.open(BytesIO(image))
            
            img_id = cosine_dist(image)
            
            return img_id

        else:
            return "Invalid Credentials"

    else:
        return 'This is GET method'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8083, debug=True)
