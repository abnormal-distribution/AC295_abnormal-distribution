from flask import Flask, render_template, request
import sys
import requests

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def mainm():
    if request.method == 'POST':  # User clicked submit button
        image_name = request.form['content'] # Get image name submitted by user
        image_file = requests.post(url=db_url, json={'image_name': image_name}) # request image file from database
        full_filename = 'http://0.0.0.0:32500' + image_file.content.decode("utf-8")
        return render_template('searchResult.html',
                               title=image_name,
                               image_url=full_filename) # render html with image
    else:
        return render_template('index.html') # first page


if __name__ == "__main__":
    # determine what the URL for the database should be, port is always 8082 for DB
    if (len(sys.argv) == 2):
        db_url = 'http://' + sys.argv[1] + ':8082'
    else:
        db_url = "http://0.0.0.0:8082/"

    app.run(host='0.0.0.0', port=8081, debug=True)
