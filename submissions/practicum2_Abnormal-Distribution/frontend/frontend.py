from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from transformers import BertTokenizer
import cv2

answer_list = list(pd.read_csv("static/data/answers.csv", index_col=0).index)

app = Flask(__name__)

def create_test_pipeline(image, question):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',do_lower_case=True)

    question_token = tokenizer.encode_plus(
        question, 
        add_special_tokens = True, # add [CLS], [SEP]
        max_length = 24, # max length of the text that can go to BERT (<=512)
        padding='max_length',
        return_attention_mask = True, # add attention mask to not focus on pad tokens
        truncation='longest_first',
        return_tensors="tf"
    )

    question_input = question_token['input_ids'].numpy()
    question_type = question_token['token_type_ids'].numpy()
    question_attention = question_token['attention_mask'].numpy()

    image = cv2.resize(image, (224, 224)).reshape(1,224,224,3)

    return (image, (question_input, question_type, question_attention))


@app.route('/', methods=['POST', 'GET'])
def index():
	# sample images & corresponding questions
	images = ["static/images/COCO_train2014_000000496617.jpg", "static/images/COCO_train2014_000000099956.jpg", "static/images/COCO_train2014_000000072906.jpg"]
	question1 = ["Is the woman working in an office?", "How many chairs are empty?", "How many people have ponytails?", "Other (Input your question below)"]
	question2 = ["Is this inside?", "How many birds do you see in the air?", "Was this photo taken at night?", "Other (Input your question below)"]
	question3 = ["Is it sunny?", "Does the weather appear to be rainy?", "Other (Input your question below)"]

	# defaults
	selections = [question1[0], question2[0], question3[0]]
	input_questions = ["", "", ""]
	answers = ["", "",""]

	if request.method == 'POST':
		# detect which images are the users asking for (by looking at which submit button was clicked)
		if 'submit1' in request.form: #image1
			idx = 0
		elif 'submit2' in request.form: #image2
			idx = 1
		elif 'submit3' in request.form: #image3
			idx = 2
		selections[idx] = request.form['Q']

		#user input their own question
		if selections[idx] == "Other (Input your question below)": 
			input_questions[idx] = request.form['content']
			preprocessed_input = create_test_pipeline(image = cv2.imread(images[idx]), question = input_questions[idx])

		# user chose question from drom-down selections
		else: 
			preprocessed_input = create_test_pipeline(image = cv2.imread(images[idx]), question = selections[idx])

		# print(input) #debug
		# predicted_answer = model.predict(input)[0] 
		# answer_index = np.argmax(predicted_answer) 
		# answers[idx] = answer_list[answer_index]

		return render_template("index.html", 
			images = images, 
			questions = [question1, question2, question3], 
			selections = selections,
			input_questions = input_questions,
			answer= answers
			)

	else:
		# print("This is the get method.")
		return render_template("index.html", 
			images = images, 
			questions = [question1, question2, question3], 
			selections = selections,
			input_questions = input_questions,
			answer= answers
			)

if __name__ == "__main__": 
    app.run(debug=True)
