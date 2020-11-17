## Front End Page

### Overview

This module contains the code that build the front end interface - a single webpage that display 3 sample images from MSCOCO dataset.
For each image, there is a drop down selections of questions to choose from. Users can also select the option *'Other'* and then type in their own question in the input box below.  
Once the user click the button *Ask!*, the model will display the predicted answer for the given question.

### Usage

`docker build -t frontend -f Docker_frontend .`

`docker run -it -p 8081:8081 frontend`
