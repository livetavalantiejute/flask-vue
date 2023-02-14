from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import json
import uuid
import os

load_dotenv()

fileObject = open("data.json", "r")
jsonContent = fileObject.read()
dataList = json.loads(jsonContent)

app = Flask(__name__, static_folder='../frontend/fronted/dist', static_url_path='/')

app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def greetings():
    return app.send_static_file('index.html')



# GET and POST route handler
@app.route('/test', methods=['GET', 'POST'])
def test():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        dataList.append({
            'id': uuid.uuid4.hex,
            '1': post_data.get('1'),
            '2': post_data.get('2'),
            '3': post_data.get('3')
        })
        response_object['message'] = 'Added!'
    else:
        response_object['data'] = dataList
    # response_object.headers.add('Access-Control-Allow-Origin', '*')
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
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
