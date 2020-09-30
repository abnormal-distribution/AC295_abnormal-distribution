from flask import Flask, request
from .similarity import cosine_similarity

app = Flask(__name__)


@app.route("/",methods=['POST','GET'])
def mainm():
    if request.method=='POST':
        image = request.get_json()['image'] # Retrieve the image submitted by the user

        img_id = cosine_similarity(image)
        
        return img_id

    else:
        return 'This is GET method'


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)
