import os
from flask import Flask, jsonify

from ProcessData import ProcessData
from RawData import RawData
from Watson import Watson


config = {
    "api_key": 'c3701f52114fce9b3de6e4e3ef7505119ac7336f',
    "password": "78zYzMEv87Xf",
    "username": "2747da81-393b-4c7c-8e6b-6568f1983e3b"
}
watson = Watson(config)

rd = RawData()
rd.get_data_file()

pd = ProcessData(rd, watson, gather_data=False, use_static_data=True)
pd.process_all()

app = Flask(__name__, static_folder='static')


@app.route('/')
def Welcome():
    return app.send_static_file('index.html')


@app.route('/api/mentions/<search_movie>')
def mentions_program(search_movie):
    reputation = pd.get_data(search_movie)
    content_obj = { 'movie_name' : search_movie, 'reputation' : reputation}
    response = jsonify(content_obj)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/people/<name2>')
def SayHello(name):
    result = watson.get_analysis('https://fee.org/articles/thanksgiving-was-a-triumph-of-capitalism-over-collectivism/')
    return jsonify(result)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
