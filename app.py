from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/home/')
def homepage():
    return 'This app is used to get gists of any Github User, to get info about any user use /gists/username path in url', 200

@app.route('/gists/<username>')
def get_user_gists(username):
      url = f'https://api.github.com/users/{username}/gists'
      try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
           gists = response.json()
           return jsonify(gists)
        else:
            return jsonify({"error": "please pass a existing user"}), 404
      except Exception as e:
        return jsonify({"error": "Internal Server error"}), 500
      #gists = response.json()
      #return jsonify(gists)

#@app.route('/<path:invalid_path>')
#def handle_invalid_path(invalid_path):
#    return 'Invalid path. Please use /gists/username path in URL.', 404

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=8080)
