from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class image_meta(db.Model):
    # file_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)

db.create_all()
db.session.commit()

@app.before_first_request
def populate_db():
	csv_url ="static/images/gap_images/metadata.csv"
	with open(csv_url) as csv_file:
		data = csv.reader(csv_file, delimiter=',')
		first_line = True
		for row in data:
			if not first_line:
				file_id = row[0]
				artist = row[1]
				title = row[2]
				query = image_meta(file_id = file_id, artist=artist, title=title)
				db.session.add(query)
				db.session.commit()
			else:
				first_line = False


@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		try:
			search_content = request.form['content']
			file_id = "gap_"+search_content+".jpg"
			file_url = "static/images/gap_images/gap_images/"+file_id
			image = db.session.query(image_meta).filter(image_meta.file_id==file_id).first()
			image_title = image.title
			# subtitle = image.artist 
			return render_template("searchResult.html", image_url=file_url, title=image_title, 
				# subtitle=subtitle
				)
		except:
			error_msg = 'Oh no! The image does not exist. '
			# subtitle = 'Please input the image file id (e.g. 11111, 11120, etc.). '
			file_id = "static/images/puppy.jpg"
			return render_template("searchResult.html", image_url=file_id, title=error_msg, 
				# subtitle=subtitle
				)
	else:
		return render_template("index.html")

if __name__ == "__main__": 
    app.run(debug=True)