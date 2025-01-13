from flask import Flask, send_from_directory, request, jsonify
import os
from flask_cors import CORS, cross_origin
from interface import solveBattle

app = Flask(__name__, static_folder="dist")
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serveWebPage(path):
    static_file_path = os.path.join(app.static_folder, path)

    if path and os.path.exists(static_file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/winChance', methods=['GET'])
@cross_origin()
def getBattleInfoFromForm():
    dico = solveBattle(request.args.get("battleInfo"))
    return jsonify(dico)


if __name__ == '__main__':
    # Change the current working directory to the directory of the current file
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    os.chdir(dir_name)
    # Start webapp
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
