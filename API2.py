import os
import fileinput
from flask import Flask, request, abort, jsonify, send_from_directory


UPLOAD_DIRECTORY = "/uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)

@api.route("/")
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


@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/files/<filename>/<string:o>/<string:n>", methods=["POST"])
def post_file(filename,o,n):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    with fileinput.FileInput(os.path.join(UPLOAD_DIRECTORY, filename), inplace=True) as file:
            for line in file:
              print(line.replace(o,n), end='')

    # Return 201 CREATED
    return "", 201
    return send_from_directory(os.path.join(UPLOAD_DIRECTORY), filename, as_attachment=True)


if __name__ == "__main__":
    api.run(debug=True)