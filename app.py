import os.path
from face_api import FaceApi
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

api = FaceApi(os.path.curdir)
app = Flask(__name__)
api.train_from_root()


@app.route('/faces', methods=['GET', 'POST', 'DELETE'])
def web_faces():
    # POST/DELETE

    if request.method == 'POST':
        if 'id' not in request.args:
            raise BadRequest("Identifier for the face was not given!")
        api.add_face(request.args['id'], request.json['base64'])

    if request.method == 'DELETE':
        if 'id' not in request.args:
            raise BadRequest("Identifier for the face was not given!")
        api.delete_face(request.args["id"])

    return jsonify(list(api.get_all_faces().keys()))


@app.route('/find', methods=['POST'])
def find_face():
    score = api.find_face(request.json['base64'])
    return jsonify(score)


if __name__ == "__main__":
    app.run(debug=True, port=8080)


