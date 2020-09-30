from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
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

# @app.before_first_request
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

if __name__ == "__main__": 
	# query image meta
	populate_db()
	file_id = "gap_11111.jpg"
	image = db.session.query(image_meta).filter(image_meta.file_id==file_id).first()
	print(image.title)
	print(image.artist)
    # app.run(debug=True)
