import os
import fileinput
from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_DIRECTORY = "/uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)

@api.route("/",methods=["GET"])
def start():
	return "SVG_API is working...."

@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)





@api.route("/getfile", methods=["POST"])
def getfile():
     file = request.files['file']
     return file.read()


@api.route("/do_it/<string:o>/<string:n>", methods=["POST"])
def do_it(o,n):
    """Upload a file."""
    file = request.files['file']
    fname = file.filename
    data = file.read()
    path = os.path.join(UPLOAD_DIRECTORY,fname)
    with open(path, 'w') as file:
        file.write(data.decode('utf-8'))

    with open(path,'r') as f:
        data = f.read()
        x = data.replace(o,n)
    with open(path, 'w') as file:
        file.write(x)

    return send_from_directory(UPLOAD_DIRECTORY,fname)
    # Return 201 CREATED
    return "", 201




if __name__ == "__main__":
    api.run(debug=True)
