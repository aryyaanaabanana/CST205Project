#Course: CST 205
#File: Main python file for image translator
#Authors: Keshav Gupta, Aryana Beulna, Allyson Rivera, Betsy Ruiz
#Date: December 17, 2020

import cv2
import pytesseract
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import requests, uuid, json

#Set-up for API requests
subscription_key = ""
endpoint = "https://api.cognitive.microsofttranslator.com/"
location = ""
path = '/translate'
constructed_url = endpoint + path
params = {
   'api-version': '3.0',
   'from': 'en',
   'to': ['es']
}
constructed_url = endpoint + path
 
headers = {
   'Ocp-Apim-Subscription-Key': subscription_key,
   'Ocp-Apim-Subscription-Region': location,
   'Content-type': 'application/json',
   'X-ClientTraceId': str(uuid.uuid4())
}
 
body = [{
   'text' : ""
}]

app = Flask(__name__)
boostrap = Bootstrap(app)

#Function that reads the image, uses pytesseract to extract the text and writes it into a text file
def get_text_from_image(image_name):
   img = cv2.imread(image_name)
   file = open("extracted.txt", "w+")
   file.write("")
   file.close()
   file = open("extracted.txt", "a")
   text = pytesseract.image_to_string(img)
   file.write(text) 
   file.close
 
#App route for the main page where there is a form for the user to upload an image, once they do, the image is passed into the get_text_from_image() function
@app.route('/', methods=["GET","POST"])
def home():
   if request.method == "POST":
       if request.files:
           image = request.files["image"]
           get_text_from_image(str(image.filename))
           return redirect(request.url)
   return render_template('homepage.html')

@app.route('/<lang>')
def translationPage(lang):
   my_file = open('extracted.txt', 'r') 
   my_text = my_file.read()
   body[0]['text'] = my_text
   params["to"][0] = lang
   request = requests.post(constructed_url, params=params, headers=headers, json=body)
   response = request.json()
   t_text = response[0]["translations"][0]["text"]
   return render_template('secondpage.html', text=my_text, t_text=t_text)

