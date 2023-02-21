from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import json
# import uuid
import os
import numpy as np
import difflib

import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

load_dotenv()

fileObject = open("data.json", "r")
jsonContent = fileObject.read()
wordData = json.loads(jsonContent)

words = [item['word'] for item in wordData]

dataList = []
corrected_words = []

app = Flask(__name__, static_folder='../client/dist', static_url_path='/')

app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def greetings():
    return "test"

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def readImage(file_bytes):
    # convert numpy array to image
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    gray = get_grayscale(img)
    thresh = thresholding(gray)
        
    return pytesseract.image_to_string(thresh, lang="lit")


def matchWords(word):
    foundWord = difflib.get_close_matches(word.lower(), words)
    wordDict = {}
    if foundWord:
        wordDict = next((item for item in wordData if item['word'] == foundWord[0]), None)
    return wordDict


def unique(list1):
  
    # initialize a null list
    unique_list = []
  
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x and x not in unique_list:
            unique_list.append(x)

    return unique_list

# GET and POST route handler
@app.route('/test', methods=['GET', 'POST'])
def test():
    global dataList
    global corrected_words

    response_object = {'status': 'success'}
    if request.method == "POST":
        # post_data = request.get_json()

        #read image file string data
        filestr = request.files['file'].read()

        #convert string data to numpy array
        file_bytes = np.fromstring(filestr, np.uint8)
        wordsRead = readImage(file_bytes)
        dataList = wordsRead.split()
        dataList = unique(dataList)
        corrected_words = map(matchWords, dataList)
        corrected_words = unique(corrected_words)

    # else:
    response_object['data'] = list(corrected_words)
    return jsonify(response_object)

# PUT and DELETE routes
# @app.route('/data/<data_id>', methods=['PUT'])
# def single_datapoint(data_id):
#     response_object = {'status': 'success'}
#     if request.method == "PUT":
#         post_data = request.get_json()
#         remove_datapoint(data_id)
#         dataList.append({
#             'id': uuid.uuid4.hex,
#             '1': post_data.get('1'),
#             '2': post_data.get('2'),
#             '3': post_data.get('3')
#         })
#         response_object['message'] = 'Updated!'
#     return jsonify(response_object)

# # Removing data
# def remove_datapoint(data_id):
#     for datapoint in dataList:
#         if datapoint['id'] == data_id:
#             dataList.remove(datapoint)
#             return True
#         else:
#             return False




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


